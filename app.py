from sympy import Symbol, E
from sympy.plotting import plot
import streamlit as st
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application, convert_xor
from matplotlib.figure import Figure
from io import BytesIO
from matplotlib import rcParams

rcParams["svg.fonttype"] = "none"

x = Symbol("x")

user_input = st.text_input(label="Expression", value="x^2", max_chars=80)

transformations = standard_transformations + (implicit_multiplication_application, convert_xor)
try:
    expr = parse_expr(user_input, transformations=transformations, local_dict={"e": E})
except Exception:
    st.error("Invalid expression")
    st.stop()

xmin_col, xmax_col, xstep_col = st.columns(3)
xmin = xmin_col.number_input(label="xmin", value=-5, max_value=-1, step=1)
xmax = xmax_col.number_input(label="xmax", value=5, min_value=1, step=1)
xstep = xstep_col.number_input(label="xstep", value=1, min_value=1, step=1)

ymin_col, ymax_col, ystep_col = st.columns(3)
ymin = ymin_col.number_input(label="ymin", value=-5, max_value=-1, step=1)
ymax = ymax_col.number_input(label="ymax", value=5, min_value=1, step=1)
ystep = ystep_col.number_input(label="ystep", value=1, min_value=1, step=1)

try:
    graph = plot(expr, (x, xmin, xmax), xlim=(xmin, xmax), ylim=(ymin, ymax), show=False, detect_poles=True)
    graph.process_series()
except Exception as e:
    st.error(f"Cannot create graph: {e}")
    st.stop()

fig: Figure = graph.fig

ax = fig.axes[0]
ax.set_xlabel("")
ax.set_ylabel("")
ax.grid(True)
ax.set_aspect("equal")
ax.set_xticks([t for t in range(xmin, xmax + 1, xstep) if t != 0])
ax.set_yticks([t for t in range(ymin, ymax + 1, ystep) if t != 0])

st.pyplot(fig)

svg = BytesIO()
fig.savefig(svg, format="svg")
st.download_button(label="Save as SVG", data=svg.getvalue(), file_name="graph.svg", mime="image/svg+xml")
