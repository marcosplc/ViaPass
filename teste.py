class MarcosPaulo:
    def __init__(self):
        self.name = "Marcos Paulo"
        self.role = "Software Developer Intern"
        self.company = "Uni9"
        self.education = "Systems Analysis and Development"

        self.interests = [
            "Full Stack Development",
            "Artificial Intelligence",
            "Data Science",
            "Automation",
        ]

    def say_hello(self):
        print("Hello, World! 👋")
        print(f"I'm {self.name}")
        print(f"Currently working at {self.company}")
        print("Always learning and building new things!")


me = MarcosPaulo()
me.say_hello()