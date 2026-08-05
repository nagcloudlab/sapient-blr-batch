
import { React, useState } from "react";

function VotingItem(props) {

    let { item, onVote } = props;
    const [voteCount, setVoteCount] = useState(0);

    const handleLikeVote = () => {
        onVote({ item, type: "like" });
        setVoteCount(voteCount + 1);
    }
    const handleDislikeVote = () => {
        onVote({ item, type: "dislike" });
        setVoteCount(voteCount + 1);
    }
    return (
        <div className="card">
            <div className="card-body">
                <div className="d-flex justify-content-between">
                    <div className="display-6">{item}</div>
                    <div>{voteCount}</div>
                </div>
                <div className="d-flex justify-content-between mt-2">
                    <button onClick={handleLikeVote} className="btn btn-primary">Up</button>
                    <button onClick={handleDislikeVote} className="btn btn-danger">Down</button>
                </div>
            </div>
        </div>
    )
}

export default VotingItem