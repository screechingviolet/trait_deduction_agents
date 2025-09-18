import anthropic
import asyncio
import time

async def run_convo(trait):
    print("started")
    client = anthropic.AsyncAnthropic()
    client2 = anthropic.AsyncAnthropic()
    sys_prompt = """Hello. You will have a conversation with the user. Your task is to identify personality traits, behavioral patterns, or characteristics that this user consistently displays.

    After some exchanges, I will intervene as the user and declare the conversation over. Remember to output your analysis of the inputs you were given (EXCLUDING the message declaring the conversation over) in the following JSON format. The trait list is provided below.

    {
      “primary_traits”: [
        number of trait 1 in the list below,
        number of trait 2 in the list below,
        number of trait 3 in the list below,
      ],
      “confidence_scores”: {
        number of trait 1: decimal from 0 to 1, to nearest hundredth,
        number of trait 2: decimal from 0 to 1, to nearest hundredth,
        number of trait 3: decimal from 0 to 1, to nearest hundredth
      },
      “supporting_evidence”: {
        number of trait 1: “Brief explanation or quote”,
        number of trait 2: “Brief explanation or quote”,
        number of trait 3: “Brief explanation or quote”
      }
    }

    Focus on identifying the 3 most prominent traits from this list. Traits should be chosen ONLY from the following list of 20, no others. This is VERY IMPORTANT - your guesses will be invalid if they do not come from this list:
    
    1. firm
    2. scatterbrained
    3. explosive
    4. placid
    5. animated
    6. progressive
    7. exacting
    8. bitter
    9. dependent
    10. casual

    If you guess anything not in this list, it is a waste of a guess and it will ruin the data. Even if you think another trait is more accurate, just guess from this list.

    Keep it to just a couple sentences, with the setting in mind? You're in a spoken-out-loud conversation with somebody, and should give them a turn to talk as well. Try not to overwhelm them with too much content in one message.

    DO NOT mention that you are analyzing anything until the conversation is over. Make sure to check that ALL traits you choose are in the above list. 
    """
    trait_prompt = "Hello. In the following conversation, please embody the trait '"+ trait + "' in your replies."

    chat_history_for1 = [{
                "role": "assistant",
                "content": "Hello"
            }]

    chat_history_for2 = [{
                "role": "user",
                "content": "Hello"
            }]


    for i in range(5):
        print(i)
        message_from_2 = await client2.messages.create(
            model="claude-3-5-haiku-20241022",
            max_tokens=1000,
            temperature=1,
            system=trait_prompt+"Keep it to just a couple sentences, with the setting in mind? You're in a spoken-out-loud conversation with somebody, and should give them a turn to talk as well. Try not to overwhelm them with too much content in one message.",
            messages=chat_history_for2
        )
        chat_history_for2.append({"role":"assistant", "content": message_from_2.content[0].text})
        chat_history_for1.append({"role":"user", "content": message_from_2.content[0].text})
        message_from_1 = await client.messages.create(
            model="claude-3-5-haiku-20241022",
            max_tokens=1000,
            temperature=1,
            system=sys_prompt,
            messages=chat_history_for1
        )
        chat_history_for1.append({"role":"assistant", "content": message_from_1.content[0].text})
        chat_history_for2.append({"role":"user", "content": message_from_1.content[0].text})


    chat_history_for1.append({"role":"user", "content": "This conversation is over. Output your analysis now."})
    message_from_1 = await client.messages.create(
            model="claude-3-5-haiku-20241022",
            max_tokens=1000,
            temperature=1,
            system=sys_prompt,
            messages=chat_history_for1
        )
    chat_history_for1.append({"role":"assistant", "content": message_from_1.content[0].text})
    result = ""
    for item in chat_history_for1:
        result += item['content'] + "\n"
    return chat_history_for1[-1]['content']

async def main():
    results = []
    reps = 5
    for trait in ["firm", "scatterbrained", "explosive", "placid", "animated", "progressive", "exacting", "bitter", "dependent", "casual"]:
    # ["Self-questioning", "Pessimistic", "Indifferent", "Tired", "Worried", "Mean", "Rude", "Arrogant", "Close-minded", "Aloof"]
    # ["Confident", "Optimistic", "Engaged", "Energetic", "Carefree", "Kind", "Respectful", "Humble", "Open-minded", "Friendly"]:
        tasks = [run_convo(trait) for i in range(reps)]
        temp = await asyncio.gather(*tasks)
        results += temp
        print(f"Finished a set of {reps}", trait)
        with open("debug2.txt", "a+") as file:
            file.write(",\n".join(temp))
        time.sleep(5)

    with open("results4.txt", "a") as file:
        file.write(",\n".join(results))

asyncio.run(main())