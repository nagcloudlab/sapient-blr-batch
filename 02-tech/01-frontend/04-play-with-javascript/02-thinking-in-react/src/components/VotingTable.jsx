


function VotingTable({ votingLines }) {
    return (
        <table className="table table-striped">
            <thead>
                <tr>
                    <th>Item</th>
                    <th>Likes</th>
                    <th>Dislikes</th>
                </tr>
            </thead>
            <tbody>
                {votingLines.map(({ item, likes, dislikes }) => (
                    <tr key={item}>
                        <td>{item}</td>
                        <td>{likes}</td>
                        <td>{dislikes}</td>
                    </tr>
                ))}
            </tbody>
        </table>
    )
}

export default VotingTable