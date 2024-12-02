from Movements.steeringOutput import SteeringOutput

class DynamicArrive:
    """
    El comportamiento Arrive calcula la salida de dirección para que un agente llegue a una posición objetivo.
    Atributos:
        character: Kinematic.
            El agente que se está moviendo.
        target: Kinematic.
            La posición objetivo hacia la que se mueve el agente.
        maxAcceleration: float.
            La aceleración máxima que puede alcanzar el agente.
        maxSpeed: float.
            La velocidad máxima que puede alcanzar el agente.
        targetRadius: float.
            El radio alrededor del objetivo donde se considera que el agente ha llegado.
        slowRadius: float.
            El radio alrededor del objetivo donde el agente comienza a desacelerar.
        timeToTarget: float.
            El tiempo durante el cual se debe alcanzar la velocidad objetivo (por defecto es 0.1).
    Métodos:
        getSteering():
            Calcula y devuelve la salida de dirección para que el agente llegue a la posición objetivo.
            Devuelve None si el agente está dentro del targetRadius.
    """
    def __init__(self, character, target, maxAcceleration, maxSpeed, targetRadius, slowRadius, timeToTarget=0.1):
        self.character = character
        self.target = target
        self.maxAcceleration = maxAcceleration
        self.maxSpeed = maxSpeed
        self.targetRadius = targetRadius
        self.slowRadius = slowRadius
        self.timeToTarget = timeToTarget

    def getSteering(self):
        result = SteeringOutput()
        # Conseguir la dirección y la distancia al objetivo.
        direction = self.target.position - self.character.position
        distance = direction.length()
        # Si estamos dentro del targetRadius, no es necesario hacer nada.
        if distance < self.targetRadius:
            return None
        # Si estamos fuera del slowRadius, la velocidad objetivo es máxima.
        if distance > self.slowRadius:
            targetSpeed = self.maxSpeed
        # Si estamos dentro del slowRadius, la velocidad objetivo se ajusta para desacelerar.
        else:
            targetSpeed = self.maxSpeed * distance / self.slowRadius

        # La velocidad objetivo combina dirección y magnitud.
        targetVelocity = direction
        targetVelocity.normalize()
        targetVelocity *= targetSpeed
        # La aceleración intenta llegar a la velocidad objetivo.
        result.linear = targetVelocity - self.character.velocity
        # Ajustar la aceleración en función del tiempo objetivo.
        result.linear /= self.timeToTarget
        # Verificar si la aceleración es demasiado rápida y si lo es ajustarla.
        if result.linear.length() > self.maxAcceleration:
            result.linear.normalize()
            result.linear *= self.maxAcceleration
        # No hay rotación en el comportamiento Arrive.
        result.angular = 0
        return result