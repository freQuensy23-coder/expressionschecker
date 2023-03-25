from flask import Flask, request, render_template, jsonify
import sympy
from sympy.parsing.sympy_parser import parse_expr

app = Flask(__name__)

def check_equality(expr1, expr2):
    return sympy.simplify(expr1 - expr2) == 0

def _is_invalid(c):
    return c.isalpha() or c == '_'

def is_safe(inp_string):
    """ Blacklist attribute access, simply by checking for any period that is
    not surrounded by numbers. Returns True for '3.4', but not for 'a.b' """
    components = inp_string.split(".")
    if len(components) == 1:
        return True
    for c in components:
        if _is_invalid(c[0]) or _is_invalid(c[-1]):
            return False
    return True

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        expr1 = request.form['expr1']
        expr2 = request.form['expr2']
        if (not is_safe(expr1)) or (not is_safe(expr2)):
            message = "Unsafe expression"
            return jsonify({'message': message})
        expr1 = parse_expr(expr1, transformations="all")
        expr2 = parse_expr(expr2, transformations="all")
        try:
            expr1 = sympy.sympify(expr1)
            expr2 = sympy.sympify(expr2)
            result = check_equality(expr1, expr2)
            if result:
                message = "The expressions are equal."
            else:
                message = "The expressions are not equal."
            return jsonify({'message': message})
        except sympy.SympifyError:
            message = "Invalid input. Please enter a valid expression."
            return jsonify({'message': message})
    return render_template('index.html')

@app.route('/usages')
def usages():
    return render_template('usages.html')


if __name__ == '__main__':
    app.run(debug=True, port=5000)
