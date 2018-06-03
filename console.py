#from tradePlan import TradePlan
from cmd import Cmd
import datetime
import agent


class MyPrompt(Cmd):

    now = datetime.datetime.now()
    print (now.strftime("%Y-%m-%d %H:%M"))

    def do_market(self, args):
        """
        Changes context currency
        :param args: str for market currency
        """
        market = args
        agent.market(args)

    def do_plans(self, args):
        print(agent.plans)

    def do_show(self, args):
        agent.show();

    def do_capital(self, args):
        agent.capital(float(args))

    def do_entry(self, args):
        agent.entry(float(args))

    #only tests for now
    def do_execute(self, args):
        agent.execute()

    def do_save(self, args):
        agent.save()

    def do_load(self, args):
        agent.load()
        print(agent.plans)

    def do_quit(self, args):
        """Quits the program."""
        print ("Quitting.")
        raise SystemExit


if __name__ == '__main__':
    prompt = MyPrompt()
    prompt.prompt = '> '
    prompt.cmdloop('Starting prompt...')