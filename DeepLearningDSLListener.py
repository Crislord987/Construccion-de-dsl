# Generated from DeepLearningDSL.g4 by ANTLR 4.13.1
from antlr4 import *
if "." in __name__:
    from .DeepLearningDSLParser import DeepLearningDSLParser
else:
    from DeepLearningDSLParser import DeepLearningDSLParser

# This class defines a complete listener for a parse tree produced by DeepLearningDSLParser.
class DeepLearningDSLListener(ParseTreeListener):

    # Enter a parse tree produced by DeepLearningDSLParser#program.
    def enterProgram(self, ctx:DeepLearningDSLParser.ProgramContext):
        pass

    # Exit a parse tree produced by DeepLearningDSLParser#program.
    def exitProgram(self, ctx:DeepLearningDSLParser.ProgramContext):
        pass


    # Enter a parse tree produced by DeepLearningDSLParser#statement.
    def enterStatement(self, ctx:DeepLearningDSLParser.StatementContext):
        pass

    # Exit a parse tree produced by DeepLearningDSLParser#statement.
    def exitStatement(self, ctx:DeepLearningDSLParser.StatementContext):
        pass


    # Enter a parse tree produced by DeepLearningDSLParser#assignment.
    def enterAssignment(self, ctx:DeepLearningDSLParser.AssignmentContext):
        pass

    # Exit a parse tree produced by DeepLearningDSLParser#assignment.
    def exitAssignment(self, ctx:DeepLearningDSLParser.AssignmentContext):
        pass


    # Enter a parse tree produced by DeepLearningDSLParser#expressionStatement.
    def enterExpressionStatement(self, ctx:DeepLearningDSLParser.ExpressionStatementContext):
        pass

    # Exit a parse tree produced by DeepLearningDSLParser#expressionStatement.
    def exitExpressionStatement(self, ctx:DeepLearningDSLParser.ExpressionStatementContext):
        pass


    # Enter a parse tree produced by DeepLearningDSLParser#controlStructure.
    def enterControlStructure(self, ctx:DeepLearningDSLParser.ControlStructureContext):
        pass

    # Exit a parse tree produced by DeepLearningDSLParser#controlStructure.
    def exitControlStructure(self, ctx:DeepLearningDSLParser.ControlStructureContext):
        pass


    # Enter a parse tree produced by DeepLearningDSLParser#ifStatement.
    def enterIfStatement(self, ctx:DeepLearningDSLParser.IfStatementContext):
        pass

    # Exit a parse tree produced by DeepLearningDSLParser#ifStatement.
    def exitIfStatement(self, ctx:DeepLearningDSLParser.IfStatementContext):
        pass


    # Enter a parse tree produced by DeepLearningDSLParser#whileStatement.
    def enterWhileStatement(self, ctx:DeepLearningDSLParser.WhileStatementContext):
        pass

    # Exit a parse tree produced by DeepLearningDSLParser#whileStatement.
    def exitWhileStatement(self, ctx:DeepLearningDSLParser.WhileStatementContext):
        pass


    # Enter a parse tree produced by DeepLearningDSLParser#expression.
    def enterExpression(self, ctx:DeepLearningDSLParser.ExpressionContext):
        pass

    # Exit a parse tree produced by DeepLearningDSLParser#expression.
    def exitExpression(self, ctx:DeepLearningDSLParser.ExpressionContext):
        pass


    # Enter a parse tree produced by DeepLearningDSLParser#booleanExpression.
    def enterBooleanExpression(self, ctx:DeepLearningDSLParser.BooleanExpressionContext):
        pass

    # Exit a parse tree produced by DeepLearningDSLParser#booleanExpression.
    def exitBooleanExpression(self, ctx:DeepLearningDSLParser.BooleanExpressionContext):
        pass


    # Enter a parse tree produced by DeepLearningDSLParser#comparator.
    def enterComparator(self, ctx:DeepLearningDSLParser.ComparatorContext):
        pass

    # Exit a parse tree produced by DeepLearningDSLParser#comparator.
    def exitComparator(self, ctx:DeepLearningDSLParser.ComparatorContext):
        pass


    # Enter a parse tree produced by DeepLearningDSLParser#matrixOperation.
    def enterMatrixOperation(self, ctx:DeepLearningDSLParser.MatrixOperationContext):
        pass

    # Exit a parse tree produced by DeepLearningDSLParser#matrixOperation.
    def exitMatrixOperation(self, ctx:DeepLearningDSLParser.MatrixOperationContext):
        pass


    # Enter a parse tree produced by DeepLearningDSLParser#mlOperation.
    def enterMlOperation(self, ctx:DeepLearningDSLParser.MlOperationContext):
        pass

    # Exit a parse tree produced by DeepLearningDSLParser#mlOperation.
    def exitMlOperation(self, ctx:DeepLearningDSLParser.MlOperationContext):
        pass


    # Enter a parse tree produced by DeepLearningDSLParser#trigFunction.
    def enterTrigFunction(self, ctx:DeepLearningDSLParser.TrigFunctionContext):
        pass

    # Exit a parse tree produced by DeepLearningDSLParser#trigFunction.
    def exitTrigFunction(self, ctx:DeepLearningDSLParser.TrigFunctionContext):
        pass


    # Enter a parse tree produced by DeepLearningDSLParser#plotStatement.
    def enterPlotStatement(self, ctx:DeepLearningDSLParser.PlotStatementContext):
        pass

    # Exit a parse tree produced by DeepLearningDSLParser#plotStatement.
    def exitPlotStatement(self, ctx:DeepLearningDSLParser.PlotStatementContext):
        pass


    # Enter a parse tree produced by DeepLearningDSLParser#fileOperation.
    def enterFileOperation(self, ctx:DeepLearningDSLParser.FileOperationContext):
        pass

    # Exit a parse tree produced by DeepLearningDSLParser#fileOperation.
    def exitFileOperation(self, ctx:DeepLearningDSLParser.FileOperationContext):
        pass


    # Enter a parse tree produced by DeepLearningDSLParser#literal.
    def enterLiteral(self, ctx:DeepLearningDSLParser.LiteralContext):
        pass

    # Exit a parse tree produced by DeepLearningDSLParser#literal.
    def exitLiteral(self, ctx:DeepLearningDSLParser.LiteralContext):
        pass


    # Enter a parse tree produced by DeepLearningDSLParser#matrixLiteral.
    def enterMatrixLiteral(self, ctx:DeepLearningDSLParser.MatrixLiteralContext):
        pass

    # Exit a parse tree produced by DeepLearningDSLParser#matrixLiteral.
    def exitMatrixLiteral(self, ctx:DeepLearningDSLParser.MatrixLiteralContext):
        pass


    # Enter a parse tree produced by DeepLearningDSLParser#listLiteral.
    def enterListLiteral(self, ctx:DeepLearningDSLParser.ListLiteralContext):
        pass

    # Exit a parse tree produced by DeepLearningDSLParser#listLiteral.
    def exitListLiteral(self, ctx:DeepLearningDSLParser.ListLiteralContext):
        pass



del DeepLearningDSLParser