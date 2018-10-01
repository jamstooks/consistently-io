import { connect } from "react-redux";

import Settings from "../components/Settings";
import * as actions from "../actions/integrations";

const mapStateToProps = state => ({
  integrations: state.integrations,
  current: state.current
});

const mapDispatchToProps = dispatch => ({
  getIntegrations: () => dispatch(actions.getList()),
  fetchIntegration: id => dispatch(actions.getDetail(id)),
  unselect: () => dispatch(actions.deselectIntegration())
});

export default connect(
  mapStateToProps,
  mapDispatchToProps
)(Settings);
