from pathlib import Path
def save_ans(retrieval_chain):
    output_file = Path("answers.txt")

    with output_file.open("w", encoding="utf-8") as f:

        for index, question in enumerate(question, start=1):

            print(f"Processing question {index}/{len(question)}")

            try:
                response = retrieval_chain.invoke({
                    "input": question
                })

                answer = response["answer"]

                # Display
                print(f"Question: {question}")
                print(f"Answer: {answer}")
                print("-" * 60)

                # Save
                f.write(f"Question {index}: {question}\n")
                f.write(f"Answer: {answer}\n")
                f.write("-" * 60 + "\n\n")

                f.flush()

            except Exception as e:
                print(f"Error processing question: {question}")
                print(f"Error: {e}")

    print(f"All answers saved to: {output_file.resolve()}")