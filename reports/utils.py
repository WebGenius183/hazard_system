ICAO_RISK_MATRIX = {
    'A': {5: 'High', 4: 'High', 3: 'High', 2: 'Medium', 1: 'Low'},
    'B': {5: 'High', 4: 'High', 3: 'Medium', 2: 'Medium', 1: 'Low'},
    'C': {5: 'High', 4: 'High', 3: 'Medium', 2: 'Low', 1: 'Low'},
    'D': {5: 'High', 4: 'High', 3: 'Low', 2: 'Low', 1: 'Low'},
    'E': {5: 'Low', 4: 'Low', 3: 'Low', 2: 'Low', 1: 'Low'},
}

def get_risk_level(severity, probability):
    return ICAO_RISK_MATRIX[severity][probability]

def get_risk_tolerability(risk_level):
    if risk_level == 'High':
        return 'Unacceptable'
    elif risk_level == 'Medium':
        return 'Tolerable with mitigation'
    return 'Acceptable with monitoring'
    
from django.contrib.auth.models import User

def is_supervisor(user):
    if not user or not user.is_authenticated:
        return False
    return user.groups.filter(name='Supervisor').exists()
