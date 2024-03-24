import pickle
import spacy
import random
from spacy.util import minibatch, compounding
from spacy import load, displacy
from spacy.training import Example
import random
from spacy.util import minibatch, compounding

dataset = "dataset/ner_spacy_fmt_datasets_13_Jan_2021.pickle"
with open(dataset, "rb") as f:
    ner_spacy_fmt_datasets = pickle.load(f)


nlp = spacy.blank("id")
nlp.add_pipe("ner")
nlp.begin_training()
ner = nlp.get_pipe("ner")

for _, annotations in ner_spacy_fmt_datasets:
    for ent in annotations.get("entities"):
        ner.add_label(ent[2])
        break

pipe_exceptions = ["ner", "trf_wordpiecer", "trf_tok2vec"]
unaffected_pipes = [pipe for pipe in nlp.pipe_names if pipe not in pipe_exceptions]

# TRAINING THE MODEL
with nlp.disable_pipes(*unaffected_pipes):

    # Training for 30 iterations
    for iteration in range(30):

        # shuffling examples before every iteration
        random.shuffle(ner_spacy_fmt_datasets)
        losses = {}
        # batch up the examples using spaCy's minibatch
        batches = minibatch(ner_spacy_fmt_datasets, size=compounding(4.0, 32.0, 1.001))
        for batch in batches:
            # Create Example objects from the batch
            examples = []
            for text, annotation in batch:
                example = Example.from_dict(nlp.make_doc(text), annotation)
                examples.append(example)

            nlp.update(
                examples,  # batch of Example objects
                drop=0.5,  # dropout - make it harder to memorise data
                losses=losses,
            )

        print("Losses at iteration {}".format(iteration), losses)

# test
doc = nlp(
    "SELUBUNG yang menyelimuti kasus penembakan yang menewaskan Pendeta Yeremia Zanambani di Kabupaten Intan Jaya, Papua kian terkuak. Hasil investigasi Tim Gabungan Pencari Fakta (TGPF) kasus tersebut menyatakan bahwa penembakan di Intan Jaya diduga dilakukan oleh aparat keamanan."
)
doc2 = nlp("Listrik di ruang food court sering mati tiba-tiba.")
print(doc.ents)
print("Entities", [(ent.text, ent.label_) for ent in doc.ents])
print("Entities", [(ent.text, ent.label_) for ent in doc2.ents])


# save model
from pathlib import Path

output_dir = Path("dataset/nlp_id_checkpoint_2024_03_15")
nlp.to_disk(output_dir)
print("Saved model to", output_dir)
