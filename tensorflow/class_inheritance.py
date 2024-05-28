class Parent:
    def yup(self):
        print("I am a parent")

class Child(Parent):
    def yup(self):
        print("I am a child")
        super().yup()

a = Child()
b = Parent()
# a.yup()
# b.yup()
super(Child, a).yup()
