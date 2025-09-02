import os
import random
import difflib
import re
import emoji
# --- ADDED: The new, fast, offline text-to-speech library ---
import pyttsx3

# --- MODIFIED: Initialize the offline TTS engine ---
try:
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    # Search for a male voice. On Windows, the first voice is usually male (David).
    # This loop makes it more reliable across different systems.
    for voice in voices:
        if "male" in voice.name.lower() or voice.gender == 'male':
            engine.setProperty('voice', voice.id)
            break
    print("✅ Offline TTS engine with male voice initialized successfully!")
except Exception as e:
    print(f"❌ Failed to initialize TTS engine: {e}")
    engine = None


# --- REMOVED: No longer need pygame for audio playback ---

def clean_text_for_speech(text):
    """Removes emojis and special characters from the text for cleaner audio."""
    # This function is the same, just renamed for clarity
    cleaned_text = emoji.replace_emoji(text, '')
    cleaned_text = re.sub(r'={2,}|_{2,}|-{2,}|[*#`]|\[|\]|\(|\)', ' ', cleaned_text)
    return ' '.join(cleaned_text.split())


# --- MODIFIED: Replaced the complex audio playback with a simple, direct function ---
def jarvis_speak(text):
    """Prints the text and speaks it using the offline engine."""
    print(text)
    if engine:
        # Clean the text for better pronunciation
        cleaned_text = clean_text_for_speech(text)
        # Queue the text to be spoken
        engine.say(cleaned_text)
        # Play the queued text and wait until it's finished
        engine.runAndWait()


# Riddle data (unchanged)
domain_guess_riddles = [
    {
        "question": "I learn from the past without being told, Patterns in numbers, my secrets unfold. The more data I get, the smarter I grow— Guess my name, do you know?",
        "answer": "Machine Learning"
    },
    {
        "question": "I clean, I analyze, I find what's true, Turning raw numbers into insights for you. From messy spreadsheets to hidden trends,I help decision-making till the very end.",
        "answer": "Data Science"
    }
]

after_intro_riddles = [
    {
        "question": "Fuel for AI, I come in many forms,Tables, images, or text are my norms.Without me, machines would just sit still,Guess my name—I power the skill.",
        "answer": "data"
    },
    {
        "question": "I answer your questions, from facts to wit, My name ends with Generative Pre-trained Transformer in it.Who am I?",
        "answer": "chatgpt"
    },
    {
        "question": "I link language models with memory and more, Helping AI apps think, retrieve, and explore. From chatbots to agents, I build the way—Guess the framework I am today.",
        "answer": "Langchain"
    }
]


# The rest of your game logic remains exactly the same.
# It will now use the new and improved jarvis_speak function automatically.

def generate_welcome_greeting():
    """Generate a hardcoded welcome greeting."""
    return """
🤖 Hello everyone! Welcome to the GDG AIML Domain Introduction!

I'm JARVIS, your AI assistant for today's session. I'm here to guide you through 
an exciting journey of discovery about our amazing domain!

Let's start with some fun riddles to see if you can guess what we're all about! 
Are you ready to unlock the secrets of our domain? Let's begin! 🚀
    """


def evaluate_domain_answer(user_answer, correct_answer):
    """
    Evaluates if the user's answer correctly identifies the domain using a predefined list.
    """
    user_lower = user_answer.lower().strip()
    correct_lower = correct_answer.lower().strip()

    aliases = {
        "machine learning": ["machine learning", "ml", "aiml", "ai/ml", "artificial intelligence and machine learning"],
        "data science": ["data science", "ds"]
    }

    if correct_lower in aliases:
        return user_lower in aliases[correct_lower]
    return False


def generate_wrong_answer_message(attempts_left):
    """Generate encouraging message for wrong answers."""
    messages = [
        f"🤔 Not quite there yet! Think about the core technologies. You have {attempts_left} attempt(s) left!",
        f"💭 Close, but let's think more specifically. {attempts_left} attempt(s) remaining!",
        f"🎯 Good try! Consider what makes our domain unique. {attempts_left} more chance(s) to get it!"
    ]
    return random.choice(messages)


def domain_riddle_phase():
    """Handle the domain riddle phase with attempts and local evaluation."""
    jarvis_speak("\n🧩 DOMAIN DISCOVERY RIDDLES")
    jarvis_speak("=" * 40)
    jarvis_speak("Let's see if you can guess our domain! You have 2 attempts per riddle.")
    jarvis_speak("If you correctly identify AIML or Data Science, we'll move to the next phase! 🎯\n")

    domain_discovered = False
    for riddle in domain_guess_riddles:
        jarvis_speak(f"🧩 Riddle: {riddle['question']}")
        attempts = 2
        riddle_solved = False
        while attempts > 0 and not riddle_solved:
            jarvis_speak(f"\n💭 Attempts remaining: {attempts}")
            user_answer = input("🎤 Your answer: ").strip()

            if not user_answer:
                jarvis_speak("Please provide an answer!")
                continue

            if evaluate_domain_answer(user_answer, riddle['answer']):
                jarvis_speak(f"🎯 Excellent! That's absolutely correct! You've identified '{riddle['answer']}'!")
                jarvis_speak("🎉 Perfect! You've discovered our AIML domain!")
                riddle_solved = True
                domain_discovered = True
            else:
                attempts -= 1
                if attempts > 0:
                    jarvis_speak(f"❌ {generate_wrong_answer_message(attempts)}")
                else:
                    jarvis_speak(f"❌ No more attempts for this riddle.")

        if domain_discovered:
            break
        jarvis_speak(f"\n{'=' * 40}")
        jarvis_speak("🔄 Let's try the next riddle!")

    if not domain_discovered:
        jarvis_speak("\n🎓 Great effort everyone! Even though we didn't guess the exact terms,")
        jarvis_speak("you've shown great curiosity! Now the domain leads will reveal the answers!")

    return domain_discovered


def evaluate_exact_answer(user_answer, correct_answer):
    """Evaluate if user answer matches exactly (allowing for minor spelling mistakes)"""
    user_clean = user_answer.lower().strip().replace(" ", "")
    correct_clean = correct_answer.lower().strip().replace(" ", "")

    if user_clean == correct_clean:
        return True

    similarity = difflib.SequenceMatcher(None, user_clean, correct_clean).ratio()
    return similarity >= 0.85


def final_riddle_game():
    """Play the final riddle game after introductions"""
    jarvis_speak("\n🎮 FINAL RIDDLE GAME TIME!")
    jarvis_speak("=" * 50)
    jarvis_speak("Now that you know about our AIML domain, let's test your knowledge!")
    jarvis_speak("You have 3 attempts per riddle. Let's see how well you know AI/ML concepts! 🧠\n")

    total_questions = len(after_intro_riddles)
    correct_answers = 0

    for riddle_index, riddle in enumerate(after_intro_riddles):
        jarvis_speak(f"🎯 Question {riddle_index + 1}/{total_questions}:")
        jarvis_speak(f"Riddle: {riddle['question']}")

        attempts = 3
        question_solved = False

        while attempts > 0 and not question_solved:
            jarvis_speak(f"\n💭 Attempts remaining: {attempts}")
            user_answer = input("🎤 Your answer: ").strip()

            if not user_answer:
                jarvis_speak("Please provide an answer!")
                continue

            is_correct = evaluate_exact_answer(user_answer, riddle['answer'])

            if is_correct:
                jarvis_speak(f"🎉 Excellent! That's absolutely correct!")
                jarvis_speak(f"✅ The answer is indeed '{riddle['answer']}'!")
                jarvis_speak("🌟 Great job! Moving to the next question...")
                question_solved = True
                correct_answers += 1
            else:
                attempts -= 1
                if attempts > 0:
                    jarvis_speak(f"❌ Not quite right. You have {attempts} attempt(s) left. Try again!")
                else:
                    jarvis_speak(f"❌ No more attempts! The correct answer was: '{riddle['answer']}'")
                    jarvis_speak("📚 Don't worry, this helps you learn! Moving to the next question...")

        jarvis_speak(f"\n{'=' * 50}")
        if riddle_index < total_questions - 1:
            input("⏸️   Press Enter for the next question...")

    jarvis_speak(f"\n🏆 GAME COMPLETE!")
    jarvis_speak(f"📊 Your Score: {correct_answers}/{total_questions}")

    if correct_answers == total_questions:
        jarvis_speak("🎉 PERFECT SCORE! You're an AIML expert!")
    elif correct_answers >= total_questions * 0.7:
        jarvis_speak("🌟 Great job! You have excellent knowledge of AIML concepts!")
    elif correct_answers >= total_questions * 0.5:
        jarvis_speak("👍 Good effort! You're learning well about AIML!")
    else:
        jarvis_speak("📚 Keep learning! Every expert was once a beginner!")

    jarvis_speak("\n🎓 Thank you for participating in the GDG AIML Domain Introduction!")
    jarvis_speak("🚀 Keep exploring the amazing world of AI and Machine Learning!")

    return {
        "total_questions": total_questions,
        "correct_answers": correct_answers,
        "score_percentage": (correct_answers / total_questions) * 100
    }


def generate_goodbye_message(game_score=None):
    """Generate a hardcoded goodbye message."""
    score_line = ""
    if game_score:
        score_line = f"You scored {game_score['correct_answers']}/{game_score['total_questions']} on the final riddles. Great work!\n"

    return f"""
🤖 Thank you all for joining the GDG AIML Domain Introduction today!

🌟 It's been wonderful seeing your curiosity and enthusiasm for AI and Machine Learning!
{score_line}
🚀 Remember, every expert was once a beginner. Keep exploring, keep learning, and 
keep building amazing things! The future is bright, and you can be part of shaping it! 

🎓 Thank you for being such an engaged audience. Until next time!

Goodbye from JARVIS! 👋✨
    """


def jarvis_final_goodbye(game_result=None):
    """Complete farewell sequence with hardcoded goodbye"""
    jarvis_speak("\n" + "=" * 60)
    jarvis_speak("🎭 JARVIS FINAL FAREWELL")
    jarvis_speak("=" * 60)
    goodbye_msg = generate_goodbye_message(game_result)
    jarvis_speak(goodbye_msg)
    jarvis_speak("\n" + "=" * 60)
    jarvis_speak("✨ Session Ended Successfully! ✨")
    return goodbye_msg


def complete_jarvis_intro():
    """Complete JARVIS introduction session with welcome and riddles"""
    jarvis_speak("🤖 JARVIS GDG AIML Domain Introduction")
    jarvis_speak("=" * 60)
    welcome_msg = generate_welcome_greeting()
    jarvis_speak(welcome_msg)
    input("\n⏸️   Press Enter when ready to start the riddles...")
    riddle_success = domain_riddle_phase()
    jarvis_speak("\n" * 2 + "=" * 60)
    if riddle_success:
        jarvis_speak("🎉 Outstanding! You've successfully identified our AIML domain!")
        jarvis_speak("🧠 You clearly understand what Machine Learning and Data Science are about!")
        jarvis_speak("✨ Now the domain leads will tell you MORE about the AIML domain -")
        jarvis_speak("📈 Advanced concepts, real-world projects, and exciting opportunities ahead!")
    else:
        jarvis_speak("🌟 Now the domain leads will tell you all about the AIML domain!")
    jarvis_speak("🎤 Domain leads, the stage is yours!")
    return {
        "riddle_phase_completed": True,
        "riddle_success": riddle_success,
        "next_phase": "domain_intro"
    }


def complete_session_with_riddles():
    """Complete JARVIS session including the final riddle game"""
    jarvis_speak("🎯 Phase 1: Domain Discovery")
    intro_result = complete_jarvis_intro()
    jarvis_speak("\n" + "=" * 60)
    jarvis_speak("⏳ Waiting for domain leads introduction...")
    input("Press Enter when domain leads have finished introducing...")
    jarvis_speak("\n" + "=" * 60)
    jarvis_speak("🤖 JARVIS: We are not forgetting the core members!")
    jarvis_speak("👥 Core members, please introduce yourselves!")
    jarvis_speak("⏳ Waiting for core members introduction...")
    input("Press Enter when core members have finished introducing...")
    jarvis_speak("\n" + "=" * 60)
    jarvis_speak("🎯 Phase 2: Knowledge Testing")
    game_result = final_riddle_game()
    jarvis_speak("\n" + "=" * 60)
    jarvis_speak("✨ GDG AIML Domain Introduction Session Complete!")
    jarvis_final_goodbye(game_result)
    return {
        "intro_phase": intro_result,
        "game_phase": game_result,
        "session_completed": True
    }


def main():
    """Main function to run the complete JARVIS session"""
    jarvis_speak("🚀 JARVIS GDG AIML Domain Introduction")
    jarvis_speak("=" * 60)
    jarvis_speak("Welcome to the interactive JARVIS session!")
    jarvis_speak("Choose an option:")
    jarvis_speak("1. Complete session (Domain discovery + Introductions + Riddle game)")
    jarvis_speak("2. Domain discovery only")
    jarvis_speak("3. Final riddle game only")
    jarvis_speak("4. Exit")

    while True:
        choice = input("\nEnter your choice (1-4): ").strip()

        if choice == "1":
            jarvis_speak("\n🎉 Starting complete JARVIS session...")
            complete_session_with_riddles()
            break
        elif choice == "2":
            jarvis_speak("\n🎉 Starting domain discovery phase...")
            complete_jarvis_intro()
            break
        elif choice == "3":
            jarvis_speak("\n🎉 Starting final riddle game...")
            game_result = final_riddle_game()
            jarvis_final_goodbye(game_result)
            break
        elif choice == "4":
            jarvis_speak("👋 Goodbye! Thanks for using JARVIS!")
            break
        else:
            jarvis_speak("❌ Invalid choice. Please enter 1, 2, 3, or 4.")


if __name__ == "__main__":
    main()