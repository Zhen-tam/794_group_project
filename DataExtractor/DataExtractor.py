import json

# Opening JSON file
f = open('dev-v1.1.json',)
ctxt_output = open("context.txt","w+")
question_output = open('questions.txt',"w+")

data = json.load(f)
entries = data['data']
# print(len(data['data']))
ctxt_cnt = 0
question_cnt = 0
for entry in entries:
    subentries = entry['paragraphs']
    for subentry in subentries:
        ctxt_output.write(subentry['context'])
        ctxt_output.write('\n')
        ctxt_cnt += 1
        qas = subentry['qas']
        for qa in qas:
            question_output.write(qa['question'])
            question_output.write('\n')
            question_cnt += 1

# Closing file
f.close()
print(ctxt_cnt)
print(question_cnt)
ctxt_output.close()
question_output.close()