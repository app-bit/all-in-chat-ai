This is a prototype to start exploring if we can build an AI Assistant which can help with a particular subject. OpenAI model is provided w/ data from a trasncript as context for Episode from `All-In podcast`
Improvements which can be done on modelling:
1. Fine-tuning the model to better manage the context in terms of size of input data.
2. Building an AI agent via [Assistants API](https://platform.openai.com/docs/assistants/overview) which can take neccessary input functions and manage function calling based on neccessary prompts.

on APP:
1.If we're building for an Org: We can use `role-based security` for authentication via [sign in process](https://firebase.google.com/docs/auth).
2. Using a real-time db we can record responses from user for running analysis such as understanding `customer`or `employee` behavior.
