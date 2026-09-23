from datetime import datetime, timezone, timedelta

# A simple Post mock model for testing integration
class Post:
    def __init__(self, post_id: str, text: str, timestamp: datetime, platform: str = "forum", author_id: str = "actor_1"):
        self.post_id = post_id
        self.text = text
        self.timestamp = timestamp
        self.platform = platform
        self.author_id = author_id

    def get(self, key, default=None):
        return getattr(self, key, default)

# Helper to generate consecutive days
def dt(days_offset: int, hour: int = 2) -> datetime:
    return datetime(2026, 1, 1, hour, 0, 0, tzinfo=timezone.utc) + timedelta(days=days_offset)

PERSONA_A_POSTS = [
    Post("A1", "this is so bs... cant believe they did this...", dt(1, 2), "dark_forum"),
    Post("A2", "we need a new plan... this one is busted...", dt(2, 3), "dark_forum"),
    Post("A3", "who got the goods? dm me...", dt(3, 2), "dark_forum"),
    Post("A4", "anyone else seeing this connection issue...?", dt(4, 4), "dark_forum"),
    Post("A5", "this node is totally compromised... stay away...", dt(5, 2), "dark_forum"),
    Post("A6", "im out... this is getting too hot...", dt(7, 3), "dark_forum"),
    Post("A7", "checking back... still dead...", dt(10, 2), "dark_forum"),
    Post("A8", "maybe tomorrow we will see some action...", dt(11, 4), "dark_forum"),
    Post("A9", "dont trust the new guy... smells like a trap...", dt(12, 3), "dark_forum"),
    Post("A10", "ill be back when things cool down...", dt(14, 2), "dark_forum"),
]

PERSONA_B_POSTS = [
    Post("B1", "this is crazy... they actually shut it down...", dt(30, 2), "new_market"),
    Post("B2", "need a reliable vendor... no scammers...", dt(31, 3), "new_market"),
    Post("B3", "the old place was better... too many feds here...", dt(33, 4), "new_market"),
    Post("B4", "anyone got the old link...? pm me...", dt(34, 2), "new_market"),
    Post("B5", "this layout is garbage... cant find anything...", dt(36, 3), "new_market"),
    Post("B6", "who remembers the 2024 bust...?", dt(38, 2), "new_market"),
    Post("B7", "hit me up if you want the real stuff...", dt(39, 4), "new_market"),
    Post("B8", "im logging off... catch you later...", dt(41, 3), "new_market"),
]

PERSONA_C_POSTS = [
    Post("C1", "Greetings everyone. I am looking for a reliable source for wholesale items.", dt(1, 10), "market"),
    Post("C2", "The current prices are unacceptable. We must negotiate better terms.", dt(2, 11), "market"),
    Post("C3", "I have reviewed the documentation. It appears to be legitimate.", dt(4, 10), "market"),
    Post("C4", "Please ensure all transactions are verified through escrow.", dt(5, 14), "market"),
    Post("C5", "I will be offline for the weekend. Direct all queries to my associate.", dt(6, 16), "market"),
    Post("C6", "The shipment has arrived successfully. Thank you for your business.", dt(9, 10), "market"),
    Post("C7", "We need to discuss the upcoming changes in security protocols.", dt(10, 11), "market"),
    Post("C8", "I advise everyone to update their encryption keys immediately.", dt(11, 10), "market"),
    Post("C9", "The previous transaction was satisfactory. I will place another order.", dt(13, 14), "market"),
    Post("C10", "Could you provide more details regarding the product specifications?", dt(14, 11), "market"),
    Post("C11", "I am unsatisfied with the delay. Please expedite the process.", dt(16, 15), "market"),
    Post("C12", "Thank you for the prompt response. We can proceed as planned.", dt(17, 10), "market"),
]
