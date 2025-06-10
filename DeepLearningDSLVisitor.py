# Generated from DeepLearningDSL.g4 by ANTLR 4.13.1
from antlr4 import *
if "." in __name__:
    from .DeepLearningDSLParser import DeepLearningDSLParser
else:
    from DeepLearningDSLParser import DeepLearningDSLParser

# This class defines a complete generic visitor for a parse tree produced by DeepLearningDSLParser.

class DeepLearningDSLVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by DeepLearningDSLParser#program.
    def visitProgram(self, ctx:DeepLearningDSLParser.ProgramContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DeepLearningDSLParser#statement.
    def visitStatement(self, ctx:DeepLearningDSLParser.StatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DeepLearningDSLParser#assignment.
    def visitAssignment(self, ctx:DeepLearningDSLParser.AssignmentContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DeepLearningDSLParser#expressionStatement.
    def visitExpressionStatement(self, ctx:DeepLearningDSLParser.ExpressionStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DeepLearningDSLParser#controlStructure.
    def visitControlStructure(self, ctx:DeepLearningDSLParser.ControlStructureContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DeepLearningDSLParser#ifStatement.
    def visitIfStatement(self, ctx:DeepLearningDSLParser.IfStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DeepLearningDSLParser#whileStatement.
    def visitWhileStatement(self, ctx:DeepLearningDSLParser.WhileStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DeepLearningDSLParser#expression.
    def visitExpression(self, ctx:DeepLearningDSLParser.ExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DeepLearningDSLParser#booleanExpression.
    def visitBooleanExpression(self, ctx:DeepLearningDSLParser.BooleanExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DeepLearningDSLParser#comparator.
    def visitComparator(self, ctx:DeepLearningDSLParser.ComparatorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DeepLearningDSLParser#matrixOperation.
    def visitMatrixOperation(self, ctx:DeepLearningDSLParser.MatrixOperationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DeepLearningDSLParser#mlOperation.
    def visitMlOperation(self, ctx:DeepLearningDSLParser.MlOperationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DeepLearningDSLParser#trigFunction.
    def visitTrigFunction(self, ctx:DeepLearningDSLParser.TrigFunctionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DeepLearningDSLParser#plotStatement.
    def visitPlotStatement(self, ctx:DeepLearningDSLParser.PlotStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DeepLearningDSLParser#fileOperation.
    def visitFileOperation(self, ctx:DeepLearningDSLParser.FileOperationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DeepLearningDSLParser#literal.
    def visitLiteral(self, ctx:DeepLearningDSLParser.LiteralContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DeepLearningDSLParser#matrixLiteral.
    def visitMatrixLiteral(self, ctx:DeepLearningDSLParser.MatrixLiteralContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DeepLearningDSLParser#listLiteral.
    def visitListLiteral(self, ctx:DeepLearningDSLParser.ListLiteralContext):
        return self.visitChildren(ctx)



del DeepLearningDSLParser