# @file decision_tree.py
# @brief Implementación de un árbol de decisión para la toma de decisiones.
# @author Anya Marcano
# @date 2024/11/05

from abc import ABC, abstractmethod

class DecisionTreeNode(ABC):
    """
    Clase base abstracta para un nodo de árbol de decisión.

    Esta clase sirve como un plano para crear nodos en un árbol de decisión.
    Cada nodo debe implementar el método `make_decision`, que define la lógica
    para tomar una decisión basada en los criterios del nodo.

    Métodos
    -------
    make_decision()
        Método abstracto que debe ser implementado por las subclases para definir el proceso de toma de decisiones.
    """
    @abstractmethod
    def make_decision(self):
        pass

class Action(DecisionTreeNode):
    """
    Clase Acción que hereda de DecisionTreeNode.
    
    Métodos
    -------
    make_decision():
        Retorna la instancia actual de la clase Acción.
    """
    def make_decision(self):
        return self

class Decision(DecisionTreeNode):
    """
    Clase que representa un nodo de decisión en un árbol de decisión.
    Atributos:
        true_node (DecisionTreeNode): El nodo a seguir si la prueba de decisión es verdadera.
        false_node (DecisionTreeNode): El nodo a seguir si la prueba de decisión es falsa.
    Métodos:
        test_value():
            Método abstracto para probar la condición de decisión. Debe ser implementado por las subclases.
        get_branch():
            Determina qué rama seguir en función de la prueba de decisión.
        make_decision():
            Toma una decisión de manera recursiva recorriendo el árbol de decisión.
    """
    def __init__(self, true_node: DecisionTreeNode, false_node: DecisionTreeNode):
        self.true_node = true_node
        self.false_node = false_node

    @abstractmethod
    def test_value(self):
        pass

    def get_branch(self):
        if self.test_value():
            return self.true_node
        return self.false_node

    def make_decision(self):
        branch = self.get_branch()
        return branch.make_decision()