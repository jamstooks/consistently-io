import profile from "./";
import mockProfileRepos from "../mockData"

describe("profile reducer", () => {
  it("should handle initial state", () => {
    expect(profile(undefined, [])).toEqual({
      isFetching: false,
      repoList: null,
      error: null
    });
  });

  it("should handle PROFILE_REQUEST", () => {
    expect(
      profile({
        isFetching: false,
        repoList: null,
        error: null
      }, {
        type: "PROFILE_REQUEST"
      })
    ).toEqual({
      isFetching: true,
      repoList: null,
      error: null
    });
  });

  it("should handle PROFILE_SUCCESS", () => {
    expect(
      profile({
        isFetching: true,
        repoList: null,
        error: null
      }, {
        type: "PROFILE_SUCCESS",
        repoList: mockProfileRepos
      })
    ).toEqual({
      isFetching: false,
      repoList: mockProfileRepos,
      error: null
    });
  });

  it("should handle PROFILE_FAILURE", () => {
    expect(
      profile({
        isFetching: true,
        repoList: null,
        error: null
      }, {
        type: "PROFILE_FAILURE",
        error: "ERROR!"
      })
    ).toEqual({
      isFetching: false,
      repoList: null,
      error: "ERROR!"
    });
  });
});
