import random
from operator import mul

def find_solution(
        pizza_pool: list[str],
        pizzas_in_solution: int,
        preferencies: dict[int:set[str]],
        allergies: dict[int:set[str]],
        iterations: int,
        steps: int,
        metrics_coefs=(1, 1),
        save_results=False
        ) -> tuple[list[str], tuple[float, float], list[float, tuple[float, float], list[str]]]:
    
    def evaluate_solution(
            solution: dict[str:int],
            allergies: dict[int:set[str]],
            preferencies: dict[int:set[str]],
            steps: int = 1000
        ) -> tuple[float, float]:

        def init_distribution():
            distribution = { user_id: { pizza_name: 0 for pizza_name in solution } for user_id in allergies }
            for pizza, pizza_amount in solution.items():
                if len(pizza_lovers[pizza]) > 0:
                    for user_id in pizza_lovers[pizza]:
                        distribution[user_id][pizza] += steps * pizza_amount // len(pizza_lovers[pizza])
                    continue
                for user_id in pizza_eaters[pizza]:
                    distribution[user_id][pizza] += steps * pizza_amount // len(pizza_eaters[pizza])
            return distribution

        def total_slices(user_id: int):
            return sum(pizza_distribution[user_id].values())

        def choose_pizza_to_share(from_id: int, to_id: int, preferencies_only: bool) -> None|str:
            if preferencies_only:
                for pizza, amount in pizza_distribution[from_id].items():
                    if amount > 0 and pizza in preferencies[to_id]:
                        return pizza
                return None
            res = None
            for pizza, amount in pizza_distribution[from_id].items():
                if amount == 0 or pizza in allergies[to_id]:
                    continue
                if pizza not in preferencies[from_id]:
                    return pizza
                res = pizza
            return res

        def choose_share_step(preferencies_only: bool) -> tuple:
            from_id, to_id, pizza_to_share = -1, -1, None
            for sharer_id in pizza_distribution:
                if from_id != -1 and total_slices(sharer_id) < total_slices(from_id):
                    continue
                for acceptor_id in pizza_distribution:
                    if sharer_id == acceptor_id or total_slices(sharer_id) - total_slices(acceptor_id) <= 1:
                        continue
                    pizza_to_share_candidate = choose_pizza_to_share(sharer_id, acceptor_id, preferencies_only)
                    if pizza_to_share_candidate != None:
                        from_id, to_id, pizza_to_share = sharer_id, acceptor_id, pizza_to_share_candidate
                    if pizza_to_share_candidate != None and preferencies_only:
                        return from_id, to_id, pizza_to_share_candidate
            
            return from_id, to_id, pizza_to_share

        def exchange_pizza(preferencies_only: bool) -> None:
            from_id, to_id, pizza = choose_share_step(preferencies_only)
            if from_id == -1:
                return False
            pizza_distribution[from_id][pizza] -= 1
            pizza_distribution[to_id][pizza] += 1
            return True

        def calculate_metrics(round_num=3) -> tuple[float, float]:
            a = [total_slices(i) for i in pizza_distribution]
            minmax = 1 - (max(a) - min(a)) / (steps * sum(solution.values()))

            satisfaction = 0
            for user_id, slices_distribution in pizza_distribution.items():
                for pizza, pizza_amount in slices_distribution.items():
                    if pizza in preferencies[user_id]:
                        satisfaction += pizza_amount
            satisfaction /= steps * sum(solution.values())
            return round(minmax, round_num), round(satisfaction, round_num)

        pizza_lovers = {
            pizza: {user_id for user_id in preferencies if pizza in preferencies[user_id]}
                for pizza in solution
        }
        pizza_eaters = {
            pizza: {user_id for user_id in allergies if pizza not in allergies[user_id]}
                for pizza in solution
        }
        pizza_distribution = init_distribution()
        
        while exchange_pizza(True):
            pass

        while exchange_pizza(False):
            pass

        res = calculate_metrics()
        
        return res

    def gen_random_solution(pool: list[str], pizza_amount: int) -> list:
        res = dict()
        for i in range(pizza_amount):
            pizza = random.choice(pool)
            if pizza in res:
                res[pizza] += 1
            else:
                res[pizza] = 1
        return res

    def eval_metrics(metrics, coefs):
        return round(sum(map(mul, metrics, coefs)), 3)
    
    best_metrics = (0, 0)
    best_solution = None
    solutions_list = []

    for i in range(iterations):
        cur_solution = gen_random_solution(pizza_pool, pizzas_in_solution)
        cur_metrics = evaluate_solution(
            cur_solution,
            allergies,
            preferencies,
            steps=steps
        )
        if save_results:
            solutions_list.append((cur_solution, cur_metrics, eval_metrics(cur_metrics, metrics_coefs)))
        if eval_metrics(cur_metrics, metrics_coefs) > eval_metrics(best_metrics, metrics_coefs):
            best_metrics = cur_metrics
            best_solution = cur_solution
    
    return best_solution, best_metrics, sorted(solutions_list, key = lambda t: t[2], reverse=True)

def usage_example():
    pizza_pool = ['Pepperoni', 'Cheese', 'Grill', 'Carbonara', 'Pesto']
    pizzas_in_solution = 3
    users_amount = 5 # not used, all users should be provided through preferencies and allergies
    allergies = {
        0: set(),
        1: {'Carbonara'},
        2: {'Cheese'},
        3: set(),
        4: set()
    }
    preferencies = {
        0: {'Pesto'},
        1: {'Pesto', 'Pepperoni'},
        2: set(),
        3: {'Grill'},
        4: set()
    }
    optimal_solution = find_solution(
        pizza_pool,
        pizzas_in_solution,
        preferencies,
        allergies,
        iterations=100,
        steps=1000,
        metrics_coefs=(2, 1),
        save_results=True
    )
    print(f"Best solution: {optimal_solution[0]}")
    print(f"Best solution metrics (equality of food distribution, overall satisfaction): {optimal_solution[1]}")
    print(f"Top 10 solutions:")
    for i in optimal_solution[2][:10]:
        print(i)

# usage_example()