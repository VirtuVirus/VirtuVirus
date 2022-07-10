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

As of now, there are no official releases of VirtuVirus. The easiest way to obtain VirtuVirus is to grab the latest executable from the Actions tab.
You can see *pyinstaller* jobs in that tab : access the commit you want to use, download the artifact adapted for your system, and run the executable.
Currently, the executables provided are for Windows and Linux.

In the event you cannot/don't want to use them, it is possible to manually run the Python code straight from source.

## Requirements (when using source)
- *Python 3.10*
- *Tkinter (with the Ttk module)*
- *pip (optional, use it to install the other dependencies)*
- *Matplotlib*
- *Pillow*

To install the necessary dependencies, you can use the following command, if *pip* is properly setup on your system :
```
pip install -r requirements.txt
```

## How do I use it ?

When running from source, go to the root of the folder and run in a terminal :
```
python3 VirtuVirus.py
```
When using an executable, run it as you usually would run one on your system. Note that on Windows, you'll have to run the executable from its folder specifically. The executables will need to unpack their dependencies (and decompress them on Windows), so **allow some time for them to load**.

Following these steps, you'll be able to access and use the VirtuVirus interface. Here's the buttons available and what they do :
- **Start** : This button will start the simulation upon being pressed, you'll need to have them spawned using *"Modify Settings"* first.
- **Stop** : This button will permanently stop the currently running simulation if pressed. You won't be able to resume it, and you'll have to clear it before starting a new simulation.
- **Pause/Resume** : This button allows you to pause the simulation, or to resume it if it's already paused.
- **Modify Settings** : The most important button in the interface, since it allows you to spawn a simulation after configuring its **many** settings. Those settings can be about the agents themselves, their behavior, how the simulation will run, or how the virus will act.
- **Show Graph** : This button will spawn a "Graph Selection" window, letting you choose through multiple settings before generating a graph using Matplotlib according to your choices.

As of now, the current types of agents are :
- 🔵 **Sane** : This agent has yet to be infected. It possesses no resistance to the infection, and will rush less often to the center the more infected agents there are.
- 🔴 **Infected** : This poor agent just got infected, either by being spawned because of you or by catching the infection from another agent. They will always avoid rushing to the center, as they know they represent a danger : on every frame, any agent in their range has a chance to be infected ! 
- 🟢 **Immune** : Luckily, they got over the infection, since the chance for them to recover slowly increases over time. They won't bother evading their needs anymore, since they can't get sick again... for now.
- ⚪ **Dead** : Some, however, are less lucky. They do not survive their infection, and will die, stopping any movement. Notice how the more infected agents there are, the more deaths happens : it is meant to represent public health services becoming overloaded.

Additionally, agents can take other colors under certain conditions :
- 🟣 **Infected (Symptomless)** : If *"Enable symptomless agents"* is enabled, some agents will be defined as "Symptomless" upon spawning. That means that if they become Infected, they will never be taken to Quarantine. Symtomless agents also cannot die, and so the only outcome for them is to become immune eventually.
- 🟡 **Central travel** : If *"Make central travel obvious"* is enabled in the settings, any type of agent currently performing central travelling will temporarily use this color instead. This makes it extremely easy to notice agents using this behavior.

## F.A.Q

### Both the program and the source refuse to run on Linux when using Wayland.

Your terminal is incompatible. Use another terminal.

Known incompatible terminals :
- xfce4-terminal

### The interface is frozen, what can I do ?

*VirtuVirus* can be an heavy program to run, to the point where the interface can freeze if the simulation becomes too intense for your processor. In case that happens, *VirtuVirus* will always automatically pause the simulation when there are no more infected agents : this allows the interface to eventually catch up with the simulation, unfreezing the program and allowing you to generate a graph.

## Bug Reports / Contributions / Suggestions
You can report bugs or suggest features by making an issue, or you can contribute to this program directly by forking it and then sending a pull request. Any help will be very much appreciated. Thank you for your time.
