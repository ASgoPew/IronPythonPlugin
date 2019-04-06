using IronPython.Hosting;
using IronPython.Runtime;
using IronPython.Runtime.Operations;
using Microsoft.Scripting.Hosting;
using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using Terraria;
using TerrariaApi.Server;

namespace IronPythonTests
{
    public class kek : TerrariaPlugin
    {
        public virtual void donothing()
        {

        }

        public void lmao()
        {
            Console.WriteLine("EPICCCCCCCC");
        }

        public kek(Main game) : base(game)
        {
        }

        public override void Initialize()
        {
            throw new NotImplementedException();
        }
    }

    public static class ex
    {
        public static void f(this kek k)
        {
            Console.WriteLine("OH MAH GAH");
        }
    }

    public class Program
    {
        public delegate void LolD(int p);
        public static event LolD Event;

        public static ScriptEngine engine = Python.CreateEngine();
        public static ScriptScope scope = engine.CreateScope();

        public static void um(object sender, TShockAPI.GetDataHandlers.ChestOpenEventArgs args)
        {

        }

        static void Main(string[] args)
        {
            //MemoryStream
            //for (int i = 0; i < 3; i++)
            //engine.Execute("l = [i for i in range(10000000)]", engine.CreateScope());
            //GC.WaitForFullGCComplete();
            ServerApi.Hooks.NetGetData.Register(new kek(null), _ => { Console.WriteLine("ayyyyyy"); });
            engine.Execute("print('started')", scope);
            Task.Run(() =>
            {
                try
                {
                    engine.ExecuteFile("test.py", scope);
                    Event(5);
                    ServerApi.Hooks.NetGetData.Invoke(new GetDataEventArgs());
                    TShockAPI.GetDataHandlers.ChestOpen += um;
                    TShockAPI.GetDataHandlers.ChestOpen.Invoke(333, new TShockAPI.GetDataHandlers.ChestOpenEventArgs());
                    scope.GetVariable("cmdF")("THIS IS FROM PYTHON FUNCTION");
                    PythonTuple o = scope.GetVariable("tmpF")();
                    Console.WriteLine(o);
                    dynamic f = scope.GetVariable("changingF");
                    f();
                    //Console.WriteLine(DefaultContext.Default.GlobalScope);
                    //PythonCalls.Call(DefaultContext.Default, f);
                    //engine.Execute("changingF()", scope);
                    //engine.Operations.InvokeMember(f, "changingF");
                    Console.WriteLine(scope.GetVariable("asd"));
                }
                catch (Exception e)
                {
                    Console.WriteLine(e);
                }
                Console.WriteLine("OK EPIC");
                engine.Execute("print('haha lol')");
            });
            /*Task.Delay(3000).ContinueWith(_ => engine.Execute(@"
for i in range(200000):
    a_dict[i] = 'lololo';
", scope));*/

            //for (int i = 0; i < 1000; i++)
            //new Task(() => f()).Start();

            //engine.ExecuteFile("test.py", scope);

            //dynamic function = scope.GetVariable("factorial");
            // вызываем функцию и получаем результат
            //dynamic result = function(5);
            //Console.WriteLine(result);

            Console.Read();
        }

        public static void f()
        {
            engine.Execute("print('kek')");
        }
    }
}
