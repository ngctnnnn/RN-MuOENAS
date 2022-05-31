class Algorithm():
    def get_new_archive(ind_obj, archive, archive_code, ind_obj_code) -> list:
        """
        Hàm trả về archive mới với cá thể ind_obj truyền vào

        Arguments:
        ind_obj -- cá thể đang xét (pair bao gồm FLOPs, -measure)
        archive -- tập các cá thể trong archive
        archive_code -- kiểu hình của các cá thể trong archive 
        ind_obj_code -- kiểu hình của cá thể đang xét

        Returns:
        Archive mới
        """
        def is_dominated_separatedly(ind_obj, ind_archive) -> bool:
            """
            Hàm kiểm tra 1 cá thể đang xét có bị thống trị bởi 1 cá thể khác hay không

            Arguments:
            ind_obj -- cá thể đang xét
            archive -- một cá thể trong archive
            """
            condition_forall = True
            condition_exists = False

            for measure in range(len(ind_obj)):
                # f(x_1) <= f(x_2), \forall i \in len(ind)
                if ind_obj[measure] > ind_archive[measure]: 
                    condition_forall = False
                    break
            for measure in range(len(ind_obj)):
                # f(x_1) < f_(x_2), \exists i \in len(ind)
                if ind_obj[measure] < ind_archive[measure]:
                    condition_exists = True
                    break
            return condition_forall and condition_exists
        
        idx_indobj_dominated_by_archive = []

        for idx_archive in range(len(archive)):
            if is_dominated_separatedly(ind_obj, archive[idx_archive]):
                idx_indobj_dominated_by_archive.append(idx_archive)
            
            if is_dominated_separatedly(archive[idx_archive], ind_obj):
                return archive, archive_code

        archive_result = [ind_obj]
        archive_code_result = [ind_obj_code]
        for idx in range(len(archive)):
            if idx not in idx_indobj_dominated_by_archive:
                archive_result.append(archive[idx])
                archive_code_result.append(archive_code[idx])

        return archive_result, archive_code_result
