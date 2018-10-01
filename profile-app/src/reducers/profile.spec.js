import profile from "./profile";
import { mockProfileRepos } from "../testUtils/mockData"


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
        json: mockProfileRepos
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

  it("should handle TOGGLE_REQUEST", () => {

    let newMock = mockProfileRepos.slice();
    newMock[0].isFetching = true;

    expect(
      profile({
        isFetching: false,
        repoList: mockProfileRepos,
        error: null
      }, {
        type: "TOGGLE_REQUEST",
        github_id: mockProfileRepos[0].github_id
      })
    ).toEqual({
      isFetching: false,
      repoList: newMock,
      error: null
    });
  });

  it("should handle TOGGLE_SUCCESS", () => {

    let newMock = mockProfileRepos.slice();
    newMock[0].is_active = !newMock[0].is_active;

    expect(
      profile({
        isFetching: false,
        repoList: mockProfileRepos,
        error: null
      }, {
        type: "TOGGLE_SUCCESS",
        github_id: newMock[0].github_id,
        json: { is_active: newMock[0].is_active }
      })
    ).toEqual({
      isFetching: false,
      repoList: newMock,
      error: null
    });
  });

});
