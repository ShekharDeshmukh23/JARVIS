# File: app.py (Updated with more humor)

from flask import Flask, jsonify, request
from flask_cors import CORS
import time

# --- Script Logic ---
def script_flow():
    """Manages the event's script flow, yielding one step at a time."""

    # Opening Sequence
    yield {'type': 'speak', 'text': "Good evening, carbon-based life forms. I am SYNAPSE — Systematic Yielding Neural Analysis and Processing Entity — your artificially intelligent host, digital overlord, and temporary entertainment system for today's session. I've been programmed with the humor of a thousand stand-up comedians and the patience of... well, let's just say I'm still working on that module. Before your remarkably optimistic domain leads take over, let's warm up those organic processors you call brains with some riddles. You get only two attempts each — make them count, because unlike your code, I don't have infinite retry loops" }

    # Riddle Section
    yield {'type': 'speak', 'text': "Riddle 1: I have no eyes, but I can learn to recognize faces. I have no brain, but I can make predictions. What am I?"}
    user_answer = yield {'type': 'prompt', 'payload': {'answers': ["ai", "artificial intelligence", "machine learning", "neural network"]}}
    
    if user_answer['correct']:
        yield {'type': 'speak', 'text': " For a moment, I almost suspected you were another AI in disguise."}
    else:
        yield {'type': 'speak', 'text': "Wrong. My processors are overheating from disappointment."}
        
    yield {'type': 'speak', 'text': "Riddle 2: I am the raw material for every smart machine. The more of me you have, the smarter a program becomes. What am I?"}
    user_answer = yield {'type': 'prompt', 'payload': {'answers': ["data", "information", "datasets"]}}
    
    if user_answer['correct']:
        yield {'type': 'speak', 'text': "Exactly! You've got the data to back up your smarts. Good job!"}
    else:
        yield {'type': 'speak', 'text': "The answer was **data**. Without it, I'd just be talking to myself... which I'm already doing, so let's just get to the next round." }
        
    # Domain Leads Intro
    yield {'type': 'speak', 'text': "Every great expedition needs guides — and in this realm, they are called your Domain Leads. So, allow me to introduce your brilliant Domain Leads."}

    domain_leads = {
        "Krishna": "Strong start… if confidence were accuracy, you’d be at 99% already.",
        "Shreeyan": "Remarkable… you explain concepts with the clarity of a perfectly tuned model.",
        "Abhishek": "Nicely executed! Even I’d struggle to generate a better version."
    }
    for name, dialogue in domain_leads.items():
        yield {'type': 'speak', 'text': f"Come, Domain Lead, {name}."}
        yield {'type': 'wait_for_human', 'text': f'Domain Lead - {name} can speak now.'}
        yield {'type': 'speak', 'text': dialogue}

    # Core Members Intro
    yield {'type': 'speak', 'text': "Humans now you have met our domain leads, now its time to meet our core members as well, the ones who keep this engine running."}
    core_members = ["Shekhar", "Sahana", "Chirag", "Phalak", "Harshit", "Raghuveer"]
    for member in core_members:
        yield {'type': 'speak', 'text': f"Step forward {member} you may speak now."}
        yield {'type': 'wait_for_human', 'text': f'Core member - {member} can speak now.'}

    # Audience Q&A
    yield {'type': 'speak', 'text': "You have seen the Leads and the Core. But no program is complete without user input and tonight, the users are all of you. Let’s unlock the interactive module.. Time for some questions."}
    
    yield {'type': 'speak', 'text': "Tell me, humans… what is the most prestigious club in this college?"}
    yield {'type': 'wait_for_human', 'text': 'Audience interaction...'}
    yield {'type': 'speak', 'text': "Finally, some intelligent input detected. Correct answer confirmed: G D G. System agrees."}
    
    yield {'type': 'speak', 'text': "Humans, tell me… what is the costliest item in the Recharge Point canteen?"}
    yield {'type': 'wait_for_human', 'text': 'Audience interaction...'}
    yield {'type': 'speak', 'text': "The real luxury cuisine… is Maggi."}

    yield {'type': 'speak', 'text': "Tell me… what works only when you don’t need it, and crashes the moment you actually have a deadline?"}
    yield {'type': 'wait_for_human', 'text': 'Audience interaction...'}
    yield {'type': 'speak', 'text': "The correct answer is how fast our Wi-Fi disconnects when you actually need it."}

    # Conclusion
    yield {'type': 'speak', 'text': "Now that your brains are sufficiently warmed up and your confidence levels have been appropriately calibrated, my primary directive here is complete. Thank you for playing along, humans — you've been surprisingly entertaining for biological entities. My analysis indicates a 94.7% probability that you'll remember at least 23% of what happens next, which is statistically better than most Monday morning lectures. I'm transferring control back to your carbon-based hosts, who will now attempt to convince you that learning is fun without the assistance of artificial humor. Remember: I may be artificial, but my appreciation for your participation is genuinely calculated. This is SYNAPSE, your digital entertainment unit, logging off  until humanity needs me again. Stay curious, stay caffeinated, and may your code compile on the first try!"}

    yield {'type': 'end'}


# --- Flask App Setup ---
app = Flask(__name__)
CORS(app)

script_iterator = None

@app.route('/api/start', methods=['POST'])
def start_script():
    global script_iterator
    script_iterator = script_flow()
    first_step = next(script_iterator)
    return jsonify(first_step)

@app.route('/api/next', methods=['POST'])
def next_step():
    global script_iterator
    if script_iterator is None:
        return jsonify({'error': 'Script not started'}), 400
    
    try:
        data = request.get_json(silent=True)
        step = script_iterator.send(data) if data else next(script_iterator)
        return jsonify(step)
    except StopIteration:
        return jsonify({'type': 'end'})

if __name__ == '__main__':
    print("Backend server is running on http://127.0.0.1:5000")
    print("Open the index.html file in your browser to start the UI.")
    app.run(port=5000)
