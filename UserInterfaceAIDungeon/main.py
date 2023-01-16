from flask import Flask, render_template, request, jsonify, redirect, url_for
import json

app = Flask(__name__)

import os
import sys

from generator.gpt2.gpt2_generator import *
from story.story_manager import *
from story.utils import *

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"

setSelected = None
playerSelected = None
name = None
Start = False


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/2')
def index1():

    setting = []
    for i, sets in enumerate(settings):
        set = {}
        print_str = sets
        if setting == "fantasy":
            print_str += " (recommended)"
        else:
            print_str += " (experimental)"
        set['ids'] = i
        set['setting'] = str(print_str)
        print(set['setting'])
        setting.append(set)

    return render_template('formule.html', setting=setting)



@app.route('/AI', methods=['POST'])
def AI():
    result = request.get_json()
    message = json.loads(result)
    result = message["msg"]

    global Start
    if Start == 0 and result == "Start":
        Start = True
        if story_manager.story != None:
            del story_manager.story

        setting_description = data["settings"][setSelected]["description"]
        character = data["settings"][setSelected]["characters"][playerSelected]
        context = "You are " + name + ", a " + playerSelected + " " + setting_description + \
                  "You have a " + character["item1"] + " and a " + character["item2"] + ". "
        prompt_num = np.random.randint(0, len(character["prompts"]))
        prompt = character["prompts"][prompt_num]

        story_manager.start_new_story(prompt, context=context, upload_story=upload_story)

        return jsonify({'AImsg': context + str(story_manager.story)})

    else :
        action = result
        if action == "restart":
            del story_manager.story
            redirect(url_for("/2"))
        elif action == "quit":
            exit()
        elif action == "revert":

            if len(story_manager.story.actions) == 0:
                return jsonify({'AImsg': "You can't go back any farther. "})


            story_manager.story.actions = story_manager.story.actions[:-1]
            story_manager.story.results = story_manager.story.results[:-1]
            return jsonify({'AImsg': "Last action reverted. "})

            if len(story_manager.story.results) > 0:
                return jsonify({'AImsg': story_manager.story.results[-1]})
            else:
                return jsonify({'AImsg':story_manager.story.story_start})

        elif action == "":
            action = ""

        elif action[0] == '"':
            action = "You say " + action

        else:
            action = action.strip()
            action = action[0].lower() + action[1:]

            action = first_to_second_person(action)

            if "You" not in action:
                action = "You " + action

            if action[-1] not in [".", "?", "!"]:
                action = action + "."

            action = "\n> " + action + "\n"

        result = "\n" + story_manager.act(action)

        if player_won(result):
            return jsonify({'AImsg': result + "\n CONGRATS YOU WIN" })
        elif player_died(result):

            return jsonify({'AImsg':"YOU DIED. GAME OVER"})


        else:
            return jsonify({'AImsg': result})

@app.route('/setting', methods=['POST'])
def update():
    global setSelected
    choice = request.form['response']
    choice = int(choice)
    if choice >= 0 and choice < len(settings) +1:
        setSelected = list(settings)[choice]
    else:
        return redirect(url_for("/2"))

    setting_key = list(settings)[choice]

    characters = data["settings"][setting_key]["characters"]

    players = []
    for i, character in enumerate(characters):
        player = {}
        player['ids'] = i
        player['player'] = str(character)
        players.append(player)
    return render_template('formule2.html', players=players)


@app.route('/player', methods=['POST'])
def update2():
    global playerSelected
    choice = request.form['response']
    choice = int(choice)
    characters = data["settings"][setSelected]["characters"]
    if choice >= 0 and choice < len(characters):
        playerSelected = list(characters)[choice]
    else:
        return redirect(url_for("/setting"))

    return render_template('formule3.html',)


@app.route('/name', methods=['POST'])
def update3():
    global name
    choice = request.form['response']
    name = choice

    print(setSelected, playerSelected, name)
    return redirect('/')

if __name__ == '__main__':


    with open("../story/story_data.yaml", 'r') as stream:
        data = yaml.safe_load(stream)
    settings = data["settings"].keys()

    upload_story = True
    generator = GPT2Generator()
    story_manager = UnconstrainedStoryManager(generator)

    app.debug = True
    app.run()
