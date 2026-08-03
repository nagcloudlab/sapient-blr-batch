
import Clock from './Clock';

function Board() {
    return (
        <div className="row">
            <div className="col-4">
                <Clock timeZone="America/New_York" />
            </div>
            <div className="col-4">
                <Clock timeZone="Europe/London" />
            </div>
            <div className="col-4">
                <Clock timeZone="Asia/Tokyo" />
            </div>
        </div>
    );
}

export default Board;