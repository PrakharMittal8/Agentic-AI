from agent import run_agent

while True:

    question = input("Ask: ")

    if question.lower() == "exit":

        break

    answer = run_agent(question)

    print("Agent:", answer)
 