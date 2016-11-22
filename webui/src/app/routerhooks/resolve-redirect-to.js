/**
 * Created by yeting on 16/7/23.
 */
///**
// * Created by yeting on 16/7/13.
// */
//import { ngModule } from '../index.module.js';
//
///**
// * Adds a custom global "redirectTo" transition hook.
// *
// * This hook will be triggered if the destination state has a 'redirectTo' property.
// * The hook will return a new TargetState based on the value of the original destination
// * state's 'redirectTo' property.
// * The Transition will then be redirected to the new TargetState.
// */
//ngModule.run(($state, $transitions) => {
//  'ngInject';
//
//  // Matches if the destination state has a 'redirectTo' property
//  const matchCriteria = { to: (state) => state.redirectTo != null };
//
//  // Function that returns a redirect for a transition, with a TargetState
//  // created using the destination state's 'redirectTo' property
//  const redirectFn = ($transition$) => {
//    'ngInject';
//    const options = $transition$.options();
//    options.location = 'replace';
//
//    return $state.target($transition$.to().redirectTo, $transition$.params(), options);
//  };
//
//  // Register the global 'redirectTo' hook
//  $transitions.onBefore(matchCriteria, redirectFn);
//});

export const resolveRedirectToRunBlock = ($transitions, $state) => {
  'ngInject';
  const matchCriteria = { to: state => state.resolve != null };

  const redirectFn = (transition) => {
    'ngInject';
    return transition.promise
      .catch(e => {
        if (e && e.redirectTo) {
          $state.go(e.redirectTo, {}, { inherit: false });
        }
        return e;
      });
  };

  $transitions.onError(matchCriteria, redirectFn);
};
