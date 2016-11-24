/**
 * Created by yeting on 16/7/13.
 */

export const authHookRunBlock = ($transitions) => {
  'ngInject';

  // Matches if the destination state's data property has a truthy 'requireAuth' property
  const requiresAuthCriteria = {
    to: (state) => state.data && state.data.requireAuth,
  };

  // Function that returns a redirect for the current transition to the login state
  // if the user is not currently authenticated (according to the AuthService)
  const redirectToLogin = (transition) => {
    const AuthService = transition.injector().get('AuthService');
    const $state = transition.router.stateService;
    if (!AuthService.isAuthenticated()) {
      return $state.target('login', undefined, { location: false });
    }
  };

  // Register the "requires auth" hook with the TransitionsService
  $transitions.onBefore(requiresAuthCriteria, redirectToLogin, { priority: 10 });
};

/**
 * This file registers an hook with the TransitionsService which protects a
 * route that requires authentication.
 *
 * Register a hook which redirects to /login when:
 * - The user is not authenticated
 * - The user is navigating to a state that requires authentication
 */
//ngModule.run();
