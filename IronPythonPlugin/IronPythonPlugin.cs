using MyIronPython;
using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Reflection;
using System.Text;
using System.Text.RegularExpressions;
using System.Threading.Tasks;
using Terraria;
using TerrariaApi.Server;
using TShockAPI;

namespace IronPythonPlugin
{
    [ApiVersion(2, 1)]
    public class IronPythonPlugin : TerrariaPlugin
    {
        #region Data

        public override string Author => "ASgo";
        public override string Description => "Plugin that provides IronPython to server development";
        public override string Name => "IronPythonPlugin";
        public override Version Version => new Version(1, 0, 0, 0);

        public static IronPythonPlugin Instance = null;
        public static string[] IronPythonEnv = new string[Main.maxPlayers + 1];
        public static Dictionary<string, object> Data = new Dictionary<string, object>();
        private static MethodInfo TextFieldSetter = null;
        private static MethodInfo CommandFieldSetter = null;

        #endregion

        #region Initialize

        public IronPythonPlugin(Main game) : base(game)
        {
            Instance = this;
            Order = 1000;

            IronPythonConfig.Load();
        }

        public override void Initialize()
        {
            ServerApi.Hooks.ServerChat.Register(this, OnServerChat);
            ServerApi.Hooks.ServerCommand.Register(this, OnServerCommand);

            Commands.ChatCommands.Add(new Command(new List<string> { IronPythonConfig.ControlPermission }, IronPythonCommand, "py")
            {
                AllowServer = true,
                HelpText = "IronPython control"
            });

            InitializeEnvironments(TSPlayer.Server);
        }

        #endregion
        #region Dispose

        protected override void Dispose(bool disposing)
        {
            if (disposing)
            {
                ServerApi.Hooks.ServerChat.Deregister(this, OnServerChat);
                ServerApi.Hooks.ServerCommand.Deregister(this, OnServerCommand);
            }
            DisposeEnvironments(TSPlayer.Server);
            base.Dispose(disposing);
        }

        #endregion
        #region Hook handlers

        public static void OnServerChat(ServerChatEventArgs args)
        {
            TSPlayer player = TShock.Players[args.Who];
            if (!player.HasPermission(IronPythonConfig.ExecutePermission) || args.Handled)
                return;
            args.Handled = CheckIronPythonInput(player, args.Text);

            // Replacing script result inside of chat messages
            MatchCollection matches;
            if (args.Handled)
                return;
            if (TextFieldSetter == null)
                TextFieldSetter = args.GetType().GetProperty("Text").GetSetMethod(true);
            try
            {
                if ((matches = Regex.Matches(args.Text, IronPythonConfig.InlineCodeWithScriptRegex)).Count > 0)
                    TextFieldSetter.Invoke(args, new object[] { player.PyEnv().ProcessText(args.Text, matches,
                        IronPythonConfig.InlineOutputColorHEX, true, IronPythonConfig.InlineScriptColorHEX,
                        new object[] { player }) });
                if ((matches = Regex.Matches(args.Text, IronPythonConfig.InlineCodeRegex)).Count > 0)
                    TextFieldSetter.Invoke(args, new object[] { player.PyEnv().ProcessText(args.Text, matches,
                        IronPythonConfig.InlineOutputColorHEX, false, IronPythonConfig.InlineScriptColorHEX,
                        new object[] { player }) });
            } catch (Exception e)
            {
                args.Handled = true;
                PrintError(player, player.PyEnv(), e);
            }
        }

        public static void OnServerCommand(CommandEventArgs args)
        {
            if (args.Handled)
                return;
            args.Handled = CheckIronPythonInput(TSPlayer.Server, args.Command);

            // Replacing script result inside of console commands
            MatchCollection matches;
            if (args.Handled)
                return;
            if (CommandFieldSetter == null)
                CommandFieldSetter = args.GetType().GetProperty("Command").GetSetMethod(true);
            try
            {
                if ((matches = Regex.Matches(args.Command, IronPythonConfig.InlineCodeWithScriptRegex)).Count > 0)
                    CommandFieldSetter.Invoke(args,
                        new object[] { TSPlayer.Server.PyEnv().ProcessText(args.Command, matches,
                        null, true, null, new object[] { TSPlayer.Server }) });
                if ((matches = Regex.Matches(args.Command, IronPythonConfig.InlineCodeRegex)).Count > 0)
                    CommandFieldSetter.Invoke(args,
                        new object[] { TSPlayer.Server.PyEnv().ProcessText(args.Command, matches,
                        null, false, null, new object[] { TSPlayer.Server }) });
            } catch (Exception e)
            {
                args.Handled = true;
                PrintError(TSPlayer.Server, TSPlayer.Server.PyEnv(), e);
            }
        }

        public static bool CheckIronPythonInput(TSPlayer player, string text)
        {
            IronPythonEnvironment pyEnv = player.PyEnv();
            if (text.StartsWith(IronPythonConfig.CommandSpecifier) && pyEnv != null)
            {
                RunIronPython(player, pyEnv, text.Substring(IronPythonConfig.CommandSpecifier.Length));
                return true;
            }
            return false;
        }

        public static void RunIronPython(TSPlayer player, IronPythonEnvironment pyEnv, string command)
        {
            Task.Run(() => RunIronPythonThread(player, pyEnv, command));
        }

        public static void RunIronPythonThread(TSPlayer player, IronPythonEnvironment pyEnv, string command)
        {
            try
            {
                pyEnv.RunScript(command, player);
            }
            catch (Exception e)
            {
                PrintError(player, pyEnv, e);
            }

            //if (player.HasPermission(IronPythonConfig.ControlPermission))
                //pyEnv.UpdateHooks();
        }

        public static void InitializeEnvironments(TSPlayer player)
        {
            foreach (var pair in IronPythonConfig.Environments)
                if (!InitializeEnvironment(pair.Value, player))
                    break;
        }

        public static bool InitializeEnvironment(IronPythonEnvironment pyEnv, TSPlayer player)
        {
            try
            {
                pyEnv.Initialize(player, IronPythonConfig.IronPythonPath);
                return true;
            }
            catch (Exception e)
            {
                PrintError(player, pyEnv, e);
                return false;
            }
        }

        public static void DisposeEnvironments(TSPlayer player)
        {
            foreach (var pair in IronPythonConfig.Environments)
                DisposeEnvironment(pair.Value, player);
        }

        public static bool DisposeEnvironment(IronPythonEnvironment pyEnv, TSPlayer player)
        {
            try
            {
                pyEnv.Dispose();
                return true;
            }
            catch (Exception e)
            {
                PrintError(player, pyEnv, e);
                return false;
            }
        }

        #endregion
        #region IronPythonCommand

        public static void IronPythonCommand(CommandArgs args)
        {
            if (args.Parameters.Count == 0)
            {
                HelpIronPythonCommand(args);
                return;
            }
            switch (args.Parameters[0].ToLower())
            {
                case "reset":
                    ResetIronPythonCommand(args);
                    break;
                case "select":
                    SelectIronPythonCommand(args);
                    break;
                case "reload":
                    ReloadIronPythonCommand(args);
                    break;
                case "help":
                    HelpIronPythonCommand(args);
                    break;
                default:
                    HelpIronPythonCommand(args);
                    break;
            }
        }

        public static void ResetIronPythonCommand(CommandArgs args)
        {
            if (args.Parameters.Count == 1)
            {
                IronPythonEnvironment py = args.Player.PyEnv();
                if (!DisposeEnvironment(py, args.Player))
                    return;
                if (!InitializeEnvironment(py, args.Player))
                    return;
                args.Player.SendSuccessMessage($"IronPython[{py.Name}] has been reset.");
            }
            else if (args.Parameters.Count == 2)
            {
                if (args.Parameters[1].ToLower() == "all")
                {
                    foreach (var pair in IronPythonConfig.Environments)
                    {
                        if (!DisposeEnvironment(pair.Value, args.Player))
                            return;
                        if (!InitializeEnvironment(pair.Value, args.Player))
                            return;
                    }
                    args.Player.SendSuccessMessage($"All IronPythons have been reset.");
                    return;
                }

                if (!IronPythonConfig.Environments.ContainsKey(args.Parameters[1]))
                {
                    args.Player.SendErrorMessage("No such environment.");
                    return;
                }
                IronPythonEnvironment py = IronPythonConfig.Environments[args.Parameters[1]];
                if (!DisposeEnvironment(py, args.Player))
                    return;
                if (!InitializeEnvironment(py, args.Player))
                    return;
                args.Player.SendSuccessMessage($"IronPython[{py.Name}] has been reset.");
            }
        }

        public static void SelectIronPythonCommand(CommandArgs args)
        {
            if (args.Parameters.Count != 2)
            {
                args.Player.SendErrorMessage("Usage: /py select <py index>");
                return;
            }
            else if (!IronPythonConfig.Environments.ContainsKey(args.Parameters[1]))
            {
                args.Player.SendErrorMessage("No such environment.");
                return;
            }
            IronPythonEnv[args.Player.Index >= 0 ? args.Player.Index : Main.maxPlayers] = args.Parameters[1];
            args.Player.SendSuccessMessage($"Shifting to py[{args.Player.PyEnv().Name}]");
        }

        public static void ReloadIronPythonCommand(CommandArgs args)
        {

        }

        public static void HelpIronPythonCommand(CommandArgs args)
        {
            args.Player.SendInfoMessage("Usage: /py <reset/select/reload/help>");
        }

        #endregion
        #region GetData

        public static object GetData(string key)
        {
            object result;
            lock (Data)
            {
                Data.TryGetValue(key, out result);
                return result;
            }
        }

        #endregion
        #region SetData

        public static void SetData(string key, object value)
        {
            lock (Data)
                Data[key] = value;
        }

        #endregion
        #region PrintError

        public static void PrintError(TSPlayer player, IronPythonEnvironment pyEnv, Exception e)
        {
            try
            {
                if (pyEnv.CallFunctionByName("perror", e) == null)
                {
                    //player.SendErrorMessage(e.ToString());
                    player.SendErrorMessage(pyEnv.GetExceptionTraceback(e));
                }
            }
            catch (Exception e2)
            {
                player.SendErrorMessage($"Error at perror: {e2}");
                player.SendErrorMessage(e.ToString());
            }
        }

        #endregion
    }
}
