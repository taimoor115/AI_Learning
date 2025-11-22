import tiktoken 




encoding = tiktoken.encoding_for_model("gpt-4o")


text = "Hey My nae is Taimoor Hussain!"
tokens = encoding.encode(text)

print(f"Tokens: {tokens}")


decoder = encoding.decode(tokens)
print(f"Decoded Text: {decoder}")