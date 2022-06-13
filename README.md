# VirtuVirus

![VirtuVirus Logo](./assets/icon.ico)

Virus Simulator in Python *(ETIS Internship Project, organized by CY Tech and CY Cergy Paris Université)*.

Made by [JordanViknar](https://github.com/JordanViknar) and [Charx19](https://github.com/Charx19).

## Summary

- [Downloading](#How-to-download-)
- [Requirements](#Requirements-when-using-source)
- [Usage](#How-do-I-use-it-)
- [F.A.Q](#FAQ)
- [Contribute](#Bug-Reports--Contributions--Suggestions)

## How to download ?

As of currently, there are no official releases of VirtuVirus. The current way to get VirtuVirus is to either run it from source, or to grab the latest executable from the Actions tab.
Currently, the executables provided are for Windows and Linux.

In the event you cannot/don't want to use them, it is possible to manually run the Python code straight from source.

## Requirements (when using source)
- *Python 3.4 or above*
- *Tkinter (with the Ttk module)*

All other dependencies should be already bundled with Python.

## How do I use it ?

It is quite simple. Upon starting the program, you'll notice the presence of a blank canvas with some controls on the right.
Here's the description of what each button does :
- **Add agents** : This button will add 10 sane agents to the canvas. They will roam around, bounce off the borders, and occasionally rush to the center.
- **Add infected agent** : This button wil add a single infected agent to the canvas. 
- **Toggle Central Behavior** : This button will enable or disable the occasional "center rush" movement of the agents. That movement is meant to be a reproduction of people reuniting in different places, such as a school, a restaurant, a theater, etc.
- **Stop** : The simulation is (almost) immediately stopped. There is currently no way to resume it.
- **Clear** : The simulation is reset to zero and the canvas is cleaned off any agent.

As of now, the current types of agents are :
- 🔵 **Sane** : This agent has yet to be infected. It possesses no resistance to the infection, and will rush less often to the center the more infected agents there are.
- 🔴 **Infected** : This poor agent just got infected, either by being spawned because of you or by catching the infection from another agent. They will always avoid rushing to the center, as they know they represent a danger : on every frame, any agent in their range has a chance to be infected !
- 🟢 **Immune** : Luckily, they got over the infection, since the chance for them to recover slowly increases over time. They won't bother evading their needs anymore, since they can't get sick again... for now.
- ⚪ **Dead** : Some, however, are less lucky. They do not survive their infection, and will die, stopping any movement. Notice how the more infected agents there are, the more deaths happens : it is meant to represent public services becoming overloaded.

## F.A.Q

### Both the program and the source refuse to run on Linux when using Wayland ! What do I do ?

Tkinter's Wayland support is quite buggy. Weirdly enough, I've noticed that running Tkinter programs using Visual Studio Code's terminal fixes this issue. Perhaps other terminals will also properly work.

## Bug Reports / Contributions / Suggestions
You can report bugs or suggest features by making an issue, or you can contribute to this program directly by forking it and then sending a pull request. Any help will be very much appreciated. Thank you for your time.
