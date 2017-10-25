import re
import os
from jinja2 import Environment, PackageLoader, select_autoescape, FileSystemLoader
env = Environment(
    loader=FileSystemLoader('templates')
)


class LetterClassifier(object):

    def __init__(self, class_name):
        self.class_name = class_name
        self.__regs = []

    def add_reg(self, reg, score):
        self.__regs.append((reg, score))

    def score_letter(self, letter):
        score, matches = self.__score_letter(letter)
        return score

    def __score_letter(self, letter):
        current_score = 0
        matches = []
        for reg, score in self.__regs:
            match = re.search(reg, letter)
            if match:
                current_score += score
                matches.append((match, score))
        return current_score, matches

    def generate_report(self, patient_ids, letters, labels, output_folder='.'):
        failures = []
        for i, letter in enumerate(letters):
            label = labels
            score, matches = self.__score_letter(letter)
            if score > 0 != label:
                failures.append({'patient_id':patient_ids[i], 'letter':letter, 'label':label, 'score':score, 'matches':matches})

        template = env.get_template('report.html')
        for i, failure in enumerate(failures):
            output = template.render(failures=failures, current_failure=failure)
            with open(os.path.join(output_folder, "failure{}.html".format(i+1)), "w") as fh:
                fh.write(output)


if __name__ == '__main__':
    test = LetterClassifier('excited')
    test.add_reg('excited', 5)
    test.add_reg('happy', 2)
    test.add_reg(r"can't\ssleep", 3)
    test.add_reg('sad', -5)

    #print(test.score_letter("I am so excited, I can't sleep!"))
    test.generate_report([45, 34], ['I am so excited', 'so unhappy'], [False, False])