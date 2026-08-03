function LoginPage() {
    return (
        <section className="row justify-content-center">
            <div className="col-12 col-md-7 col-lg-5">
                <div className="card border-0 shadow-sm">
                    <div className="card-body p-4">
                        <h2 className="h4 mb-3">Login</h2>
                        <form>
                            <div className="mb-3 text-start">
                                <label htmlFor="email" className="form-label">Email</label>
                                <input id="email" type="email" className="form-control" placeholder="you@example.com" />
                            </div>
                            <div className="mb-4 text-start">
                                <label htmlFor="password" className="form-label">Password</label>
                                <input id="password" type="password" className="form-control" placeholder="Enter your password" />
                            </div>
                            <button type="button" className="btn btn-dark w-100">Sign In</button>
                        </form>
                    </div>
                </div>
            </div>
        </section>
    );
}

export default LoginPage;
