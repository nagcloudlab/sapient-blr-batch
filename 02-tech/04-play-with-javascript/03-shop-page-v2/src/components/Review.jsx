

function Review({ review }) {
    const totalStars = 5;
    const safeStars = Math.max(0, Math.min(review.stars, totalStars));

    return (
        <div className="card mb-3 shadow-sm border-0">
            <div className="card-body">
                <div className="d-flex justify-content-between align-items-center mb-2">
                    <div className="d-flex align-items-center gap-2">
                        <i className="fa fa-user-circle text-primary" aria-hidden="true"></i>
                        <strong>{review.author}</strong>
                    </div>
                    <div className="text-warning" aria-label={`${safeStars} out of ${totalStars} stars`}>
                        {Array.from({ length: totalStars }, (_, index) => (
                            <i
                                key={index}
                                className={`fa ${index < safeStars ? 'fa-star' : 'fa-star-o'}`}
                                aria-hidden="true"
                            ></i>
                        ))}
                    </div>
                </div>

                <p className="mb-0 text-secondary">
                    <i className="fa fa-quote-left me-2 text-muted" aria-hidden="true"></i>
                    {review.content}
                </p>
            </div>
        </div>
    );
}

export default Review;