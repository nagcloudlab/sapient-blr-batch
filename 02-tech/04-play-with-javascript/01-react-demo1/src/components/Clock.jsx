
import {
    useState,
    useEffect,
} from "react";

function Clock(props) {
    let { timeZone } = props;

    let [time, setTime] = useState(new Date().toLocaleTimeString("en-US", {
        timeZone: timeZone,
    })
    );

    useEffect(() => {
        const timer = setInterval(() => {
            setTime(
                new Date().toLocaleTimeString("en-US", {
                    timeZone: timeZone,
                })
            );
        }, 1000);

        return () => clearInterval(timer);
    }, [timeZone]);

    return (
        <div className="card">
            <div className="card-header">{timeZone}</div>
            <div className="card-body">
                <h5 className="card-title">
                    <span id={timeZone} className="badge bg-primary">
                        {time}
                    </span>
                </h5>
            </div>
        </div>
    );
}

export default Clock;