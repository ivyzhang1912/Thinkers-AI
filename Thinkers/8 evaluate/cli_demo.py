from llmtuner import ChatModel
import pandas as pd

def write_csv(path, sen, sen2):
    df = pd.DataFrame(data={'sen': sen, 'sen2': sen2})
    df.to_csv(path, mode='a', index=False, header=False)
    
def main():
    chat_model = ChatModel()
    history = []
    print("Welcome to the CLI application, use `clear` to remove the history, use `exit` to exit the application.")

    ques = list(pd.read_csv('/home/pgrad/jef/eval_3000.csv')['用户'])
    cor_a = list(pd.read_csv('/home/pgrad/jef/eval_3000.csv')['回答'])
    
    ques_l = len(ques)
    lis, q_lis, cor_lis = [], [], []
    while ques_l:
        try:
            ques_l -= 1
            query = ques[ques_l]
        
        except UnicodeDecodeError:
            print("Detected decoding error at the inputs, please set the terminal encoding to utf-8.")
            continue
        except Exception:
            raise

        if query.strip() == "exit":
            break

        if query.strip() == "clear":
            history = []
            print("History has been removed.")
            continue

        # print("Assistant: ", end="", flush=True)

        response = ""
        for new_text in chat_model.stream_chat(query, history):
            # print(new_text, end="", flush=True)
            response += new_text
        lis.append(response)
        q_lis.append(query)
        #cor_lis.append(cor_a[ques_l])

        if len(lis) % 10 == 0:
            write_csv('/home/pgrad/jef/eval_data/baichuan2-7b.csv', q_lis, lis)
            lis = []
            q_lis = []
            print('写入10')
        # history = history + [(query, response)]


if __name__ == "__main__":
    main()
