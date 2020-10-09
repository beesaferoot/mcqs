from django.db import models
from django.utils import datetime_safe


class Quiz(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField(max_length=500)
    creation_date = models.DateField(auto_created=True)
    time_frame = models.DurationField()

    class Meta:
        verbose_name_plural = "quizzes"

    def save(self, *args, **kwargs):
        self.creation_date = datetime_safe.datetime.now()
        super(Quiz, self).save(*args, **kwargs)

    def __str__(self):
        return self.title
    
    @property
    def duration(self):
        seconds = self.time_frame.seconds
        minutes = seconds // 60
        seconds = seconds % 60
        hours = minutes // 60
        minutes = minutes % 60
        return f'{hours} hr {minutes} min {seconds} sec'

class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)    
    question = models.TextField(max_length=500, default='')
    answer = models.TextField(max_length=200)

    def add_option(self, choice):
        if self.choice_set.count() == 4:
            raise Exception(f'options for question "{self}" exceeded 4')
        self.choice_set.add(choice)

    def __str__(self):
        return f'{str(self.quiz)}__question{self.pk}'
    
    
class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    content = models.TextField(max_length=200)

    def __str__(self):
        if len(str(self.content)) > 10:
            return f'{str(self.content)[:10]}...'
        return str(self.content)


class AssessmentManager(models.Manager):

    def create_assessment(self, quiz, candidate_name=None):
        if candidate_name is not None:
            instance = Assessment.objects.create(quiz=quiz, candidate_name=candidate_name)
        else:
            instance = Assessment.objects.create(quiz=quiz)
        instance.save()
        return instance

class Assessment(models.Model):
    candidate_name = models.CharField(max_length=30, default='anonymous')
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, default=None)
    start_time = models.DateTimeField(auto_created=True, auto_now=True)
    objects = AssessmentManager()
    score = models.IntegerField(default=0)
    date_taken = models.DateField(auto_created=True, auto_now=True)

    @property
    def istime_elasped(self):
        if self.start_time - datetime_safe.datetime.now() > self.quiz.time_frame:
            return True
        return False
    

    def compute_score(self, data):
        
        points = 0
        for question in self.quiz.question_set.all():
            print(f"{question.answer} == {data.get(question.question)}")
            if question.answer == data.get(question.question):
                points += 30
        print("points", points) 
        print('computed score',(points * 75) // 100)
        return (points * 75) // 100
    
    def __str__(self):
        return f'Assessment for {self.quiz}\n Date: {self.date_taken}'

    def serialize(self):
        return {
            "start_time": self.start_time.strftime("%b %-d %Y, %-I:%M %p")
        }

