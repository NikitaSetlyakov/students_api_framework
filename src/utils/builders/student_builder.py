class StudentBuilder:
    @staticmethod
    def create_student(
        email: str, 
        gender: str, 
        name: str, 
        phone_no: str, 
        status: int,
    ) -> dict:
        return {
            'email': email,
            'gender': gender,
            'name': name,
            'phone_no': phone_no,
            'status': status,
        }

    @staticmethod
    def update_student(
        email: str, 
        gender: str, 
        name: str, 
        status: int,
    ) -> dict:
        return {
            'email': email,
            'gender': gender,
            'name': name,
            'status': status,   
        }