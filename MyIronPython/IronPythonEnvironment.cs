using IronPython.Hosting;
using IronPython.Runtime;
using Microsoft.Scripting.Hosting;
using Newtonsoft.Json;
using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Text;
using System.Text.RegularExpressions;
using System.Threading.Tasks;

namespace MyIronPython
{
    public class IronPythonEnvironment
    {
        #region Data

        public static bool UseTraceback = true;

        [JsonIgnore]
        public string Name;
        [JsonProperty("directories")]
        public string[] Directories;

        [JsonIgnore]
        public static ScriptEngine Engine = Python.CreateEngine();
        [JsonIgnore]
        public ScriptScope Scope;

        [JsonIgnore]
        public Exception LastException = null;
        //private object Locker = new object();
        [JsonIgnore]
        public Dictionary<string, object> Data = new Dictionary<string, object>();

        public delegate void IronPythonExceptionD(string name, Exception e);
        public event IronPythonExceptionD IronPythonException;

        #endregion

        #region Initialize

        public bool Initialize(object me, string iron_python_path)
        {
            Scope = Engine.CreateScope();
            Scope.SetVariable("env", this);
            Scope.SetVariable("me", me);
            Scope.Engine.Execute($@"import sys
sys.path.append('{iron_python_path}\Lib')
sys.path.append('{iron_python_path}\Lib\site-packages')");

            if (!ReadEnvironment())
                return false;

            CallFunctionByName("OnInit"); // There might not be such function.

            return true;
        }

        #endregion
        #region Dispose

        public void Dispose()
        {
            if (Scope == null)
                return;
            try
            {
                CallFunctionByName("OnClose"); // There might not be such function.
            }
            catch (Exception e)
            {
                RaiseIronPythonException($"OnClose", e);
            }
        }

        #endregion
        #region operator[]

        public object this[string key]
        {
            get => Data[key];
            set => Data[key] = value;
        }

        #endregion
        #region ReadEnvironment

        public bool ReadEnvironment()
        {
            List<string> scripts = new List<string>();
            foreach (string dir in Directories)
                scripts.AddRange(Directory.EnumerateFiles(dir, "*.py", SearchOption.AllDirectories));

            scripts.Sort(delegate (string script1, string script2)
            {
                if (String.Compare(Path.GetFileNameWithoutExtension(script1), Path.GetFileNameWithoutExtension(script2)) < 0)
                    return -1;
                else if (String.Compare(Path.GetFileNameWithoutExtension(script1), Path.GetFileNameWithoutExtension(script2)) > 0)
                    return 1;
                return 0;
            });

            foreach (string script in scripts)
            {
                string filename = script.Replace(@"\", @"/");
                Console.WriteLine("\t" + filename);
                try
                {
                    Engine.ExecuteFile(filename, Scope);
                }
                catch (Exception e)
                {
                    RaiseIronPythonException("ReadEnvironment", e);
                    return false;
                }
            }
            return true;
        }

        #endregion
        #region Get

        public object Get(string name)
        {
            if (Scope.TryGetVariable(name, out object value))
                return value;
            return null;
        }

        #endregion
        #region Set

        public void Set(string name, object o = null) =>
            Scope.SetVariable(name, o);

        #endregion
        #region GenerateDotNETException

        public void GenerateDotNETException()
        {
            throw new Exception("Template ipy exception");
        }

        #endregion
        #region RunScript

        public object[] RunScript(string script, params object[] args)
        {
            object[] result;
            if (Scope.TryGetVariable("execute", out dynamic execute))
            {
                dynamic _result = execute(script, args);
                if (_result is PythonTuple tuple)
                    result = tuple.ToArray();
                else
                    result = new object[] { _result };
            }
            else
            {
                object _result = Engine.ExecuteAndWrap(script, Scope).Unwrap();
                if (_result is PythonTuple tuple)
                    result = tuple.ToArray();
                else
                    result = new object[] { _result };
            }
            return result;
        }

        #endregion
        #region CallFunction

        public object[] CallFunction(dynamic f, params object[] args) =>
            f(args) ?? new object[0];

        #endregion
        #region CallFunctionByName

        public object[] CallFunctionByName(string name, params object[] args)
        {
            if (Scope.TryGetVariable(name, out dynamic f))
                return f(args)?.ToArray() ?? new object[0];
            else
                return null;
        }

        #endregion
        #region GetExceptionTraceback

        public string GetExceptionTraceback(Exception e) =>
            Engine.GetService<ExceptionOperations>().FormatException(e);

        #endregion
        #region RaiseIronPythonException

        public void RaiseIronPythonException(string name, Exception e)
        {
            IronPythonException(name, e);
        }

        #endregion
        #region ProcessText

        public string ProcessText(string text, MatchCollection matches, string output_color, bool with_script, string script_color, params object[] args)
        {
            int matchEndIndex = 0;
            StringBuilder sb = new StringBuilder();

            foreach (Match match in matches)
            {
                sb.Append(text.Substring(matchEndIndex, match.Index - matchEndIndex));
                matchEndIndex = match.Index + match.Value.Length;
                string script = match.Groups[1].Value;
                object[] executionResult = RunScript(script, args);
                if (with_script)
                    sb.Append(PaintTerrariaOutput("<" + script + ": ", script_color));
                if (executionResult != null && executionResult.Length > 0)
                    for (int i = 0; i < executionResult.Length; i++)
                        sb.Append((i > 0 ? ", " : "") + PaintTerrariaOutput(PythonToString(executionResult[i]), output_color));
                if (with_script)
                    sb.Append(PaintTerrariaOutput(">", script_color));
            }
            sb.Append(text.Substring(matchEndIndex, text.Length - matchEndIndex));
            return sb.ToString();
        }

        public string ProcessText(string text, string pattern, string output_color, bool with_script, string script_color, params object[] args) =>
            ProcessText(text, Regex.Matches(text, pattern), output_color, with_script, script_color, args);

        #endregion
        #region PaintTerrariaOutput

        public string PaintTerrariaOutput(string text, string color)
        {
            if (color == null)
                return text;
            StringBuilder sb = new StringBuilder();
            var splitted = text.Split(']');
            for (int i = 0; i < splitted.Length - 1; i++)
                if (splitted[i].Length > 0)
                    sb.Append($"[c/{color}:{splitted[i]}][c/{color}:]]");
                else
                    sb.Append($"[c/{color}:]]");
            if (splitted[splitted.Length - 1].Length > 0)
                sb.Append($"[c/{color}:{splitted[splitted.Length - 1]}]");
            Console.WriteLine(sb.ToString());
            return sb.ToString();
        }

        #endregion
        #region PythonToString

        public string PythonToString(object o)
        {
            if (Scope.TryGetVariable("tostring", out dynamic tostring))
                return tostring(o);
            return o.ToString();
        }

        #endregion
        /*#region GenerateFunction

        public LuaFunction GenerateFunction(string code, string[] parameterNames = null, params object[] args)
        {
            code = $"return function({(parameterNames != null ? string.Join(",", parameterNames) : "")})" + code + ";end";
            object[] executionResult = RunScript(code, args);
            return executionResult?[0] as LuaFunction;
        }

        #endregion*/
        #region SharpShow

        public string SharpShow(object o)
        {
            Type type = o.GetType();
            bool typeFlag = false;
            string result = typeFlag ? type.Name + " CLASS:" : type.Name + " OBJECT:";

            if (type.GetConstructors().Length > 0)
                result += "\nCONSTRUCTORS:";
            foreach (var constructor in type.GetConstructors())
                if (constructor.IsPublic)
                {
                    string parameters = "";
                    var ps = constructor.GetParameters();
                    for (int i = 0; i < ps.Length; i++)
                    {
                        parameters += ps[i].ParameterType.Name + " " + ps[i].Name;
                        if (i != ps.Length - 1)
                            parameters += ", ";
                    }
                    result += constructor.IsStatic ? "\n   (static) " : "\n   ";
                    result += constructor.Name + " (" + parameters + ")";
                }

            if (type.GetMethods().Length > 0)
                result += "\nMETHODS:";
            foreach (var method in type.GetMethods())
                if (method.IsPublic)
                {
                    string parameters = "";
                    var ps = method.GetParameters();
                    for (int i = 0; i < ps.Length; i++)
                    {
                        parameters += ps[i].ParameterType.Name + " " + ps[i].Name;
                        if (i != ps.Length - 1)
                            parameters += ", ";
                    }
                    result += method.IsStatic ? "\n   (static) " : "\n   ";
                    result += method.ReturnType.Name + new string(' ', 10 - (method.ReturnType.Name.Length % 10)) + method.Name + " (" + parameters + ")";
                }

            if (type.GetEvents().Length > 0)
                result += "\nEVENTS:";
            foreach (var e in type.GetEvents())
                result += "\n   " + e.Name;

            if (type.GetFields().Length > 0)
                result += "\nFIELDS:";
            if (typeFlag)
            {
                foreach (var field in type.GetFields())
                    if (field.IsPublic)
                    {
                        if (field.IsStatic)
                            result += "\n   (static) " + field.Name + ": " + new string(' ', 30 - (field.Name.Length % 30)) + field.GetValue(null) ?? "null";
                        else
                            result += "\n   " + field.Name;
                    }
            }
            else
                foreach (var field in type.GetFields())
                    if (field.IsPublic)
                        result += "\n   " + field.Name + ": " + new string(' ', 30 - (field.Name.Length % 30)) + field.GetValue(o) ?? "null";
            return result;
        }

        #endregion
    }
}
