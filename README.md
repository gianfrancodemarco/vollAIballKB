Backend for the project vollAIball.
The Unity Project is [here](https://github.com/gianfrancodemarco/vollAIball).

This project explores the realm of applying artificial intelligence (AI) techniques to train autonomous agents at the game of volleyball. 
It consists of a Unity 3D environment, crafted on purpose, where agents are trained using the ML-Agents library and the Proximal Policy Optimization (PPO) algorithm. 
Another vital component of the project is the Prolog Knowledge Base, acting as a narrator that provides detailed insights into the game’s events.
These two main components are glued together by using a Python backend and rest APIs. 
This project allowed to explore the possibility of integrating different AI systems, using modern tech stacks and providing variegated features.

<br>
<div style="text-align:center">
  <img src="docs/imgs/software_architecture%20(1).jpg" alt="Software architecture" width="400"/>
  <p><i>The software architecture of the project</i></p>
</div>
<br>

## Prolog Narrator
To provide dynamic and informative commentary during the game of vollAIball, a Knowledge Base implemented using SWI-Prolog is utilized.

To achieve real-time commentary in the Unity environment, a REST API is utilized to communicate
with the Prolog Knowledge Base. The Unity environment periodically polls the commentary endpoint using a 1-second interval. This ensures that the commentary information is continuously updated and available for display.

The commentary endpoint serves as the interface between the Unity environment and the Prolog Knowl-
edge Base. It provides information about all the game events, allowing the Unity environment to retrieve the latest commentary based on the registered events. 

This endpoint execute the all_narratives query against the Knowledge Base, which wraps all of the other queries, that in turn return a textual commentary of the game.

The commentary generation process involves several
steps:

- **Knowledge Base Initialization**: When the backend server is bootstrapped, all of the rules containing the reasoning and commentary logic are defined into
the Knowledge Base
- **Event Registration**: As the game progresses in the Unity environment, relevant game events, such as a successful score, a player’s action or the ball falling outside of the field are registered in the Prolog Knowledge Base. 
These events are stored as facts, representing the history of the relevant events of the game
- **Commentary Retrieval**: Using the exposed APIs,
the Unity environment retrieves commentary from
the Prolog Knowledge Base based on the registered
game events and the pre-defined rules. The extracted
information are already in a human readable format
thanks to the formatting capabilities of the Prolog
- **Display in Unity Scene**: The commentary text is
displayed on the screens placed in the Unity scene.
The Prolog commentary process enhances the overall
gaming experience by providing real-time insights and
analysis of the game events. It adds depth and immersion to the vollAIball game.
