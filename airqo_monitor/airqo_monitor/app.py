from flask import (
    Flask,
    jsonify,
    render_template,
)

from external.thingspeak import get_all_channel_ids
from get_malfunctions import get_all_channel_malfunctions

app = Flask(__name__)

@app.route('/')
def get_malfunctioning_channels():
    malfunctioning_channels = get_all_channel_malfunctions()
    # import pdb; pdb.set_trace()
    return render_template(
        "index.html",
        malfunctioning_channels=malfunctioning_channels,
    )


if __name__ == "__main__":
    app.run(debug=True)
