using MyIronPython;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using Terraria;
using TShockAPI;

namespace IronPythonPlugin
{
    public static class TSPlayerExtension
    {
        public static IronPythonEnvironment PyEnv(this TSPlayer player)
        {
            if (player.HasPermission(IronPythonConfig.ControlPermission))
            {
                string env = IronPythonPlugin.IronPythonEnv[player.Index >= 0 ? player.Index : Main.maxPlayers];
                if (env != null)
                    return IronPythonConfig.Environments[env];
                else if (IronPythonConfig.DefaultEnvironment != null)
                    return IronPythonConfig.Environments[IronPythonConfig.DefaultEnvironment];
            }
            else if (IronPythonConfig.UntrustedEnvironment != null && player.HasPermission(IronPythonConfig.ExecutePermission))
                return IronPythonConfig.Environments[IronPythonConfig.UntrustedEnvironment];
            return null;
        }
    }
}
