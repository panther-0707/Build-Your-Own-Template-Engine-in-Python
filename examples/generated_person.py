
class Person:
    """Represents a person with basic information."""
    
    def __init__(self, name, age, email):
        """Initialize Person."""
        
        self.name = name
        
        self.age = age
        
        self.email = email
        
    
    def __str__(self):
        fields = ["name={self.name!r}""age={self.age!r}""email={self.email!r}"]
        return f"Person({', '.join(fields)})"
    
    def to_dict(self):
        """Convert to dictionary."""
        return {
            
            "name": self.name,
            
            "age": self.age,
            
            "email": self.email,
            
        }
    