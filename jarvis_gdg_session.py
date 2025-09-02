import os
import random
import difflib
import re
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from gtts import gTTS
from io import BytesIO
import pygame
import threading
import emoji

# Load environment variables
load_dotenv()

# Initialize Gemini LLM
try:
    llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash-exp")
    print("✅ Gemini LLM initialized successfully!")
except Exception as e:
    print(f"❌ Failed to initialize LLM: {e}")
    llm = None

# Initialize pygame mixer for audio playback
pygame.mixer.init()

# Global variable to control audio playback
audio_playing = False

def play_audio(text):
    """Generates and plays audio from text using gTTS."""
    global audio_playing
    audio_playing = True
    try:
        # Pre-process the text to remove unwanted characters for clean audio
        cleaned_text = clean_text_for_gtts(text)

        tts = gTTS(text=cleaned_text, lang='en', tld='co.in', slow=False)
        fp = BytesIO()
        tts.write_to_fp(fp)
        fp.seek(0)
        
        # Load and play the audio
        pygame.mixer.music.load(fp)
        pygame.mixer.music.play()
        
        # Wait for playback to finish
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
    except Exception as e:
        print(f"❌ Audio playback failed: {e}")
    finally:
        audio_playing = False
        fp.close()

def clean_text_for_gtts(text):
    """Removes emojis and special characters from the text for cleaner audio."""
    # Remove emojis first
    cleaned_text = emoji.replace_emoji(text, '')
    
    # Replace special characters with spaces or remove them
    # This regex keeps letters, numbers, spaces, and basic punctuation like . , ! ?
    cleaned_text = re.sub(r'={2,}|_{2,}|-{2,}|[*#`]|\[|\]|\(|\)', ' ', cleaned_text)
    
    # Remove any extra whitespace created
    return ' '.join(cleaned_text.split())

def jarvis_speak(text):
    """Prints the original text and starts a new thread to play the cleaned audio."""
    print(text)  # This line prints the text with emojis and formatting
    # Start audio playback in a new thread, passing the original text
    audio_thread = threading.Thread(target=play_audio, args=(text,))
    audio_thread.start()

# Riddle data
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

def generate_welcome_greeting():
    """Generate a welcome greeting using Gemini LLM"""
    prompt = """
    You are JARVIS, an AI assistant for the GDG (Google Developer Groups) introduction event.
    
    Generate a warm, enthusiastic welcome message that:
    1. Introduces yourself as JARVIS
    2. Welcomes everyone to the GDG introduction session
    3. Mentions you'll be guiding them through fun riddles to discover the domain
    4. Keeps it brief but exciting
    
    Make it sound like a friendly AI assistant ready to help students.
    """
    try:
        if llm:
            response = llm.invoke(prompt)
            return response.content
        else:
            raise Exception("LLM not available")
    except Exception as e:
        # Fallback greeting if LLM fails
        return """
🤖 Hello everyone! Welcome to the GDG AIML Domain Introduction!

I'm JARVIS, your AI assistant for today's session. I'm here to guide you through 
an exciting journey of discovery about our amazing domain!

Let's start with some fun riddles to see if you can guess what we're all about! 
Are you ready to unlock the secrets of our domain? Let's begin! 🚀
        """

def evaluate_answer_with_llm(user_answer, correct_answer, question):
    """Use Gemini LLM to evaluate if user answer is close enough to correct answer"""
    user_lower = user_answer.lower().strip()
    correct_lower = correct_answer.lower().strip()
    
    if "machine learning" in correct_lower:
        acceptable_ml = ["machine learning", "ml", "aiml", "ai/ml", "artificial intelligence and machine learning"]
        return any(term == user_lower for term in acceptable_ml)
    elif "data science" in correct_lower:
        acceptable_ds = ["data science", "ds"]
        return any(term == user_lower for term in acceptable_ds)
    
    rejected_answers = [
        "analytics", "data analytics", "data analysis", "analysis", 
        "genai", "generative ai",
        "python", "programming", "coding", "statistics", "math"
    ]
    if user_lower in rejected_answers:
        return False
    
    prompt = f"""
    STRICT EVALUATION ONLY:
    Question: {question}
    Correct Answer: {correct_answer} 
    Student Answer: {user_answer}
    
    ONLY accept these EXACT answers:
    - For Machine Learning: "machine learning", "ML", "AIML", "AI/ML" 
    - For Data Science: "data science", "DS"
    
    REJECT everything else including: analytics, data analytics, data analysis, programming, statistics
    
    Answer ONLY: CORRECT or INCORRECT
    """
    try:
        if llm:
            response = llm.invoke(prompt)
            evaluation = response.content.strip().upper()
            return "CORRECT" in evaluation
        else:
            return False
    except Exception as e:
        return False

def generate_wrong_answer_message(attempts_left, riddle_answer):
    """Generate encouraging message for wrong answers without revealing the answer"""
    messages = [
        f"🤔 Not quite there yet! Think about the core technologies in our domain. You have {attempts_left} attempt(s) left!",
        f"💭 Close, but let's think more specifically about our field. {attempts_left} attempt(s) remaining!",
        f"🎯 Good try! Consider what makes our domain unique in tech. {attempts_left} more chance(s) to get it!",
        f"🔍 Think about the specific field we're focusing on today. {attempts_left} attempt(s) left!"
    ]
    return random.choice(messages)

def domain_riddle_phase():
    """Handle the domain riddle phase with attempts and LLM evaluation"""
    jarvis_speak("\n🧩 DOMAIN DISCOVERY RIDDLES")
    jarvis_speak("=" * 40)
    jarvis_speak("Let's see if you can guess our domain! You have 2 attempts per riddle.")
    jarvis_speak("If you correctly identify AIML or Data Science, we'll move to the next phase! 🎯\n")
    
    domain_discovered = False
    all_attempts_exhausted = True
    
    for riddle_index, riddle in enumerate(domain_guess_riddles):
        jarvis_speak(f"🧩 Riddle {riddle_index + 1}:")
        jarvis_speak(f"Question: {riddle['question']}")
        
        attempts = 2
        riddle_solved = False
        
        while attempts > 0 and not riddle_solved:
            jarvis_speak(f"\n💭 Attempts remaining: {attempts}")
            user_answer = input("🎤 Your answer: ").strip()
            
            if not user_answer:
                jarvis_speak("Please provide an answer!")
                continue
            
            is_correct = evaluate_answer_with_llm(user_answer, riddle['answer'], riddle['question'])
            
            if is_correct:
                jarvis_speak(f"🎯 Excellent! That's absolutely correct! You've identified '{riddle['answer']}'!")
                jarvis_speak("🎉 Perfect! You've discovered our AIML domain!")
                jarvis_speak("💡 This shows you understand the core areas we work with in AI and Machine Learning!")
                riddle_solved = True
                domain_discovered = True
                all_attempts_exhausted = False
                return True
            else:
                attempts -= 1
                if attempts > 0:
                    wrong_msg = generate_wrong_answer_message(attempts, riddle['answer'])
                    jarvis_speak(f"❌ {wrong_msg}")
                else:
                    jarvis_speak(f"❌ No more attempts for this riddle.")
                    jarvis_speak("🔄 Let's try the next riddle!")
        
        jarvis_speak(f"\n{'='*40}")
        
        if riddle_solved:
            return True
    
    if all_attempts_exhausted:
        jarvis_speak("\n🎓 Great effort everyone! Even though we didn't guess the exact terms,")
        jarvis_speak("you've shown curiosity and engagement with our domain!")
        jarvis_speak("🌟 Now the domain leads will tell you all about the AIML domain -")
        jarvis_speak("they'll reveal the answers to the riddles and explain everything!")
        jarvis_speak("📚 You'll learn about Machine Learning, Data Science, and how they shape our future!")
    
    return False

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
        
        jarvis_speak(f"\n{'='*50}")
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
    """Generate a personalized goodbye message using Gemini LLM"""
    if game_score:
        performance_context = f"""
        The students just completed a riddle game with {game_score['correct_answers']}/{game_score['total_questions']} correct answers 
        ({game_score['score_percentage']:.1f}% score).
        """
    else:
        performance_context = "The students participated in the domain introduction session."
    
    prompt = f"""
    You are JARVIS, an AI assistant concluding the GDG AIML Domain Introduction session.
    
    {performance_context}
    
    Generate a warm, inspiring farewell message that:
    1. Thanks everyone for participating in the session
    2. Encourages continued learning in AI/ML
    3. Mentions the exciting future of AIML domain
    4. Includes a motivational note about their journey ahead
    5. Signs off as JARVIS with a friendly goodbye
    6. Keep it brief but memorable
    7. Use emojis to make it engaging
    
    Make it sound like a caring AI mentor saying goodbye to students.
    """
    try:
        if llm:
            response = llm.invoke(prompt)
            return response.content
        else:
            raise Exception("LLM not available")
    except Exception as e:
        return """
🤖 Thank you all for joining the GDG AIML Domain Introduction today!

🌟 It's been wonderful seeing your curiosity and enthusiasm for AI and Machine Learning!
Whether you aced the riddles or learned something new, you've taken an important step 
into the fascinating world of AIML.

🚀 Remember, every expert was once a beginner. Keep exploring, keep learning, and 
keep building amazing things with AI and Machine Learning!

The future is bright, and with your passion for technology, you'll be part of 
shaping that future! 

🎓 Thank you for being such an engaged audience. Until next time!

Goodbye from JARVIS! 👋✨
        """

def jarvis_final_goodbye(game_result=None):
    """Complete farewell sequence with LLM-generated goodbye"""
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
    jarvis_speak("\n" + "=" * 60)
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
    jarvis_speak("\n" + "="*60)
    jarvis_speak("⏳ Waiting for domain leads introduction...")
    input("Press Enter when domain leads have finished introducing...")
    jarvis_speak("\n" + "="*60)
    jarvis_speak("🤖 JARVIS: We are not forgetting the core members!")
    jarvis_speak("👥 Core members, please introduce yourselves!")
    jarvis_speak("⏳ Waiting for core members introduction...")  
    input("Press Enter when core members have finished introducing...")
    jarvis_speak("\n" + "="*60)
    jarvis_speak("🎯 Phase 2: Knowledge Testing")
    game_result = final_riddle_game()
    jarvis_speak("\n" + "="*60)
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