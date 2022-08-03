using MyIronPython;
using Newtonsoft.Json;
using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using TShockAPI;

namespace IronPythonPlugin
{
    public class IronPythonConfig
    {
        [JsonIgnore]
        public static string DefaultScriptsDirectory = "IronPythonScripts";

        [JsonProperty("command_specifier")]
        public static string CommandSpecifier = "\\";
        [JsonProperty("control_permission")]
        public static string ControlPermission = "python.control";
        [JsonProperty("execute_permission")]
        public static string ExecutePermission = "python.execute";
        [JsonProperty("iron_python_path")]
        public static string IronPythonPath = "C:\\Program Files\\IronPython 3.4";
        [JsonProperty("default_environment")]
        public static string DefaultEnvironment;
        [JsonProperty("untrusted_environment")]
        public static string UntrustedEnvironment;
        //language=regex
        [JsonProperty("inline_code_regex")]
        public static string InlineCodeRegex = "<<(.*?)>>";
        //language=regex
        [JsonProperty("inline_code_with_script_regex")]
        public static string InlineCodeWithScriptRegex = "{{(.*?)}}";
        [JsonProperty("inline_output_color_hex")]
        public static string InlineOutputColorHEX = "ff5500";
        [JsonProperty("inline_script_color_hex")]
        public static string InlineScriptColorHEX = "ffffff";
        [JsonProperty("environments")]
        public static Dictionary<string, IronPythonEnvironment> Environments;

        #region Write

        public static void Save()
        {
            if (!Directory.Exists(DefaultScriptsDirectory))
                Directory.CreateDirectory(DefaultScriptsDirectory);
            DefaultEnvironment = "main";
            Environments = new Dictionary<string, IronPythonEnvironment>();
            Environments.Add("main", new IronPythonEnvironment()
            {
                Directories = new string[]
                {
                    DefaultScriptsDirectory
                }
            });
            string path = System.IO.Path.Combine(Directory.GetCurrentDirectory(), "iron_python_config.json");
            File.WriteAllText(path, JsonConvert.SerializeObject(new IronPythonConfig(), Formatting.Indented));
        }

        #endregion
        #region Load

        public static void Load()
        {
            string path = System.IO.Path.Combine(Directory.GetCurrentDirectory(), "iron_python_config.json");
            if (File.Exists(path))
                JsonConvert.DeserializeObject<IronPythonConfig>(File.ReadAllText(path));
            else
                Save();

            Update();
        }

        #endregion
        #region Update

        public static void Update()
        {
            if (Environments == null)
                Environments = new Dictionary<string, IronPythonEnvironment>();
            foreach (var pair in Environments)
            {
                pair.Value.Name = pair.Key;
                pair.Value.IronPythonException += (string name, Exception e) =>
                    IronPythonPlugin.PrintError(TSPlayer.Server, pair.Value, e);
                //IronPythonHookManager.Initialize(pair.Value);
            }
        }

        #endregion
    }
}
