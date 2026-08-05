
import VotingItem from "./VotingItem"
import VotingTable from "./VotingTable"

import {
    useState,
} from "react"

function VotingBox() {

    const [items, setItems] = useState([
        "react",
        "angular",
        "vue",
    ]);
    const [votingLines, setVotingLines] = useState([
        { item: "react", likes: 10, dislikes: 0 },
        { item: "angular", likes: 5, dislikes: 5 },
        { item: "vue", likes: 2, dislikes: 0 },
    ]);

    const handleVote = (event) => {
        const { item, type } = event;
        setVotingLines((prevVotingLines) => {
            return prevVotingLines.map((line) => {
                if (line.item === item) {
                    if (type === "like") {
                        return { ...line, likes: line.likes + 1 }
                    } else if (type === "dislike") {
                        return { ...line, dislikes: line.dislikes + 1 }
                    }
                }
                return line;
            })
        })
    }

    return (
        <div className="card">
            <div className="card-header">Voting Box</div>
            <div className="card-body">
                <div className="d-flex gap-3">
                    {items.map((item) => (
                        <VotingItem key={item} item={item} onVote={handleVote} />
                    ))}
                </div>
                <hr />
                <VotingTable votingLines={votingLines} />
            </div>
        </div>
    )
}

export default VotingBox