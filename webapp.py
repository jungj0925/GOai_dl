from goai.agent.naive import RandomBot
from goai.frontend.server import get_web_app

agent = RandomBot()
webapp = get_web_app({ 'random': agent })
webapp.run()