from pygame import Vector2 as Vector

class SteeringOutput:
    """
    Una clase utilizada para representar la salida de dirección de un agente.

    Atributos
    ---------
    linear : Vector
        El componente lineal de la salida de dirección. Por defecto es un vector cero si no se proporciona.
    angular : float
        El componente angular de la salida de dirección. Por defecto es 0 si no se proporciona.

    Métodos
    -------
    __init__(self, linear=None, angular=0)
        Inicializa el SteeringOutput con los valores lineales y angulares dados.
    """
    def __init__(self, linear=None, angular=0):
        self.linear = linear if linear is not None else Vector(0, 0)
        self.angular = angular