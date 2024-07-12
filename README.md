# Introduction
This is the first code I did using the Blender API. The idea behind the project is to automate animating particles that spawn when the projectile is moving in predetermined motion (already animated).

It is a limited implementation and only works for the projectiles that move up and down.

https://github.com/user-attachments/assets/ebce9ca9-47ac-4a80-b183-454834bb1fa3


# How it works
Before we delve in, we need to know the features of the implementation.
## Features
![Addon](https://github.com/user-attachments/assets/d24ba95d-23a4-47d4-b69d-24a0971b3f5d)

To spawn the particles, you must first choose which object you want so you can add the particles. 
![Choosing](https://github.com/user-attachments/assets/be5a4505-d11e-4127-a2c1-8455a0df0e3d)

Also, it is a good practice to add a notification to indicate that the system is working properly instead of guessing whether everything is fine or not.
![Notification](https://github.com/user-attachments/assets/89670e4c-5088-4e77-912a-84112135e204)

You can also delete them with a click of a button instead of going to each plane object and deleting them one by one.

**Before adding the particles.**
![Before Applying](https://github.com/user-attachments/assets/3e0d6f5d-35aa-422b-8a4f-5c2b93c0ccb6)

**After adding the particles.**
![After Apply](https://github.com/user-attachments/assets/dcd18dfa-8da0-4bff-be71-c05689dfbed8)

## Particles
When you add the particle, it calculates the apex height of the ball, spawns them, and then adds keyframes. The movement of the particle depends on how far up the ball is, and if the ball’s height apex is equal to zero, then particles won’t spawn.

**First bounce particles**
![TimelinePart1](https://github.com/user-attachments/assets/eb8825ab-98d6-4ef3-bc7b-58cbfaeb61ee)

**Second bounce particles. The distance will be closer to the ball as the impact of the ball is weaker.**
![TimelinePart2](https://github.com/user-attachments/assets/900b1855-4505-4f33-86b9-2e3903ae745e)

The rotation of the particles depends on the current active camera location.
![ObjToCam](https://github.com/user-attachments/assets/c529ae07-c193-4c1d-8207-53f7d05540f3)

![ObjToCam2](https://github.com/user-attachments/assets/5219e532-a142-4812-85bf-cefff60b49e4)

Normally particles spawn randomly, but for simplicity sake, I determined how many particles can spawn “4” and how they should move “on the x and y axes”.
![Destination](https://github.com/user-attachments/assets/19e5f521-145b-4c2f-ab39-0241b411a973)

And the particle destination depends on the ball's apex height.
![Bounce1](https://github.com/user-attachments/assets/ac3356be-19bf-4375-816e-4f47abb3d23f)

![Bounce2](https://github.com/user-attachments/assets/a46182bc-51c7-4673-a256-f2c0e464f22b)

![Bounce3](https://github.com/user-attachments/assets/c179f870-8ddb-4bc7-a3dd-363ab81f19dc)

For textures, The best workflow I thought of is that when choosing an object and spawning the particles, the code looks for a material that you want to use in the asset library and assigns it to the particles. I believe this approach is great as you can open any project, get your asset library ready, choose any material you want, and then spawn the particles.
![AssetLibrary](https://github.com/user-attachments/assets/671a4235-64d2-4bdd-9ee3-a95a5297c1bc)

A quick note regarding the textures. When creating your texture, you need to make sure that the texture has an alpha channel and the rest of the channels are set properly, so when using the texture, you can control it however you want, like using the alpha channel to hide an unwanted background. In my test, the picture wasn’t set properly, so I was stuck with the black background.😣

![Untitled-1](https://github.com/user-attachments/assets/7c4bac2c-45b0-4a01-a31b-db6295e3777d)

# sketches from a mad man.
The project required linear algebra and trigonometry, which means I had to open the whiteboard and start drawing to understand how to approach this project :)
![Plan](https://github.com/user-attachments/assets/6cec6ac1-eeb8-49fd-9a0d-172e945812c2)
