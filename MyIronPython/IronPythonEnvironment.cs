using IronPython.Hosting;
using Microsoft.Scripting.Hosting;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace MyIronPython
{
    public class IronPythonEnvironment
    {
        #region Data

        public static ScriptEngine Engine = Python.CreateEngine();

        public ScriptScope Scope;

        #endregion

        #region Initialize

        public void Initialize()
        {
            Scope = Engine.CreateScope();

            Engine.ExecuteFile("test.py", Scope);
        }

        #endregion
        #region Dispose

        public void Dispose()
        {

        }

        #endregion
    }
}
