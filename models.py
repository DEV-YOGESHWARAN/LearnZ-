from mongoengine import Document, EmbeddedDocument, StringField, ListField, EmbeddedDocumentField, EmailField, DateTimeField, ReferenceField, BooleanField
from datetime import datetime
import hashlib
import secrets

class User(Document):
    email = EmailField(required=True, unique=True)
    password_hash = StringField(required=True)
    first_name = StringField(max_length=50)
    last_name = StringField(max_length=50)
    created_at = DateTimeField(default=datetime.utcnow)
    last_login = DateTimeField()
    
    meta = {'collection': 'users'}

    def set_password(self, password):
        """Hash and set password"""
        salt = secrets.token_hex(16)
        password_hash = hashlib.pbkdf2_hmac(
            'sha256',
            password.encode('utf-8'),
            salt.encode('utf-8'),
            100000
        ).hex()
        self.password_hash = f"{salt}${password_hash}"

    def check_password(self, password):
        """Verify password"""
        if '$' not in self.password_hash:
            return False
        salt, stored_hash = self.password_hash.split('$')
        password_hash = hashlib.pbkdf2_hmac(
            'sha256',
            password.encode('utf-8'),
            salt.encode('utf-8'),
            100000
        ).hex()
        return secrets.compare_digest(password_hash, stored_hash)

class Lesson(EmbeddedDocument):
    title = StringField()
    script = StringField()

# ✅ Add Option EmbeddedDocument
class Option(EmbeddedDocument):
    text = StringField(required=True)
    correct = BooleanField(default=False)

# ✅ Add Question EmbeddedDocument
class Question(EmbeddedDocument):
    question = StringField(required=True)
    options = ListField(EmbeddedDocumentField(Option))
    explanation = StringField()

# ✅ Add Quiz EmbeddedDocument
class Quiz(EmbeddedDocument):
    title = StringField(required=True)
    questions = ListField(EmbeddedDocumentField(Question))

class Module(EmbeddedDocument):
    title = StringField()
    description = StringField()
    lessons = ListField(EmbeddedDocumentField(Lesson))
    content = StringField(default="")
    examples = ListField(StringField(), default=[])
    video_url = StringField()
    # ✅ Add quiz field to Module
    quiz = EmbeddedDocumentField(Quiz)

class Course(Document):
    title = StringField(required=True)
    topic = StringField()
    status = StringField(default="pending")
    modules = ListField(EmbeddedDocumentField(Module))
    created_by = ReferenceField(User)
    created_at = DateTimeField(default=datetime.utcnow)
    
    meta = {'collection': 'courses'}
