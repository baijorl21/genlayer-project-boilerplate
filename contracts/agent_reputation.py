
# { "Depends": "py-genlayer:1jb45aa8ynh2a9c9xn3b7qqh8sm5q93hwfp7jqmwsfhh8jpz09h6" }

from genlayer import *


@allow_storage
class AgentProfile:
    name: str
    reputation: u256
    total_rewards: u256
    contributions: u256
    active: bool


class AgentReputation(gl.Contract):
    agents: TreeMap[Address, AgentProfile]

    def __init__(self):
        pass

    @gl.public.write
    def register_agent(self, name: str) -> None:
        sender = gl.message.sender_address

        if sender in self.agents:
            raise Exception("Agent already registered")

        self.agents[sender] = AgentProfile(
            name=name,
            reputation=0,
            total_rewards=0,
            contributions=0,
            active=True,
        )

    @gl.public.write
    def add_contribution(self, points: int) -> None:
        sender = gl.message.sender_address

        if sender not in self.agents:
            raise Exception("Agent is not registered")

        if points <= 0:
            raise Exception("Points must be greater than zero")

        agent = self.agents[sender]
        agent.contributions += points
        agent.reputation += points

    @gl.public.write
    def reward_agent(self, amount: int) -> None:
        sender = gl.message.sender_address

        if sender not in self.agents:
            raise Exception("Agent is not registered")

        if amount <= 0:
            raise Exception("Reward must be greater than zero")

        self.agents[sender].total_rewards += amount

    @gl.public.write
    def deactivate_agent(self) -> None:
        sender = gl.message.sender_address

        if sender not in self.agents:
            raise Exception("Agent is not registered")

        self.agents[sender].active = False

    @gl.public.view
    def get_agent(self, agent_address: str) -> dict:
        address = Address(agent_address)

        if address not in self.agents:
            raise Exception("Agent not found")

        agent = self.agents[address]

        return {
            "address": agent_address,
            "name": agent.name,
            "reputation": agent.reputation,
            "total_rewards": agent.total_rewards,
            "contributions": agent.contributions,
            "active": agent.active,
        }

    @gl.public.view
    def get_my_profile(self) -> dict:
        sender = gl.message.sender_address

        if sender not in self.agents:
            raise Exception("Agent is not registered")

        agent = self.agents[sender]

        return {
            "address": sender.as_hex,
            "name": agent.name,
            "reputation": agent.reputation,
            "total_rewards": agent.total_rewards,
            "contributions": agent.contributions,
            "active": agent.active,
        }
